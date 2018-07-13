import functools, operator
from collections import OrderedDict

from django.utils.safestring import mark_safe

from django_pandas.io import read_frame
import pandas as pd
import numpy as np

from utils.shortcuts import csv2array, classinit


REMAIN_ORDER_COLUMN_NAME = '처방잔량'
REMAIN_AMOUNT_COLUMN_NAME = '잔량'
REMAIN_AMOUNT_UNIT_COLUMN_NAME = '단위'
ROW_COUNTER = '앰플/바이알개수'
REMAIN_AMOUNT_SUM_COLUMN_NAME = '잔량합계'


@classinit({
    'namemap_key': 'current_name',
    'namemap_value': 'mapping_to',
    'narcotic_key': 'narcotic_name',
    'narcotic_amt': 'amt',
    'narcotic_unit': 'unit',
    'config_extra_columns': 'extra_columns'
})
class OpremainDataFrame(object):

    def __init__(self, config, excel_io):
        namemaps = config.namemap_set.all()
        Narcotic = namemaps.first().mapping_to.__class__

        self.config = config
        self.df_namemaps = read_frame(namemaps)
        self.df_op = pd.read_excel(excel_io, ignore_index=True)
        self.namemapping = dict(self.df_namemaps.set_index(self.namemap_key)[self.namemap_value])
        self.df_narcotic = read_frame(Narcotic.objects.all())
        self.df_base = pd.merge(self.df_namemaps, self.df_narcotic, left_on=self.namemap_value, right_on=self.narcotic_key)

    def _validate_extra_columns(self, attr_nm):
        valid_columns = []
        columns = csv2array(getattr(self.config, attr_nm))
        for colnm in columns:
            if colnm in self.df_op.columns:
                valid_columns.append(colnm)
        return valid_columns
    
    def _get_mapped_op(self):
        df = self.df_op.copy()
        mapped = df[self.config.key_column].apply(lambda x: self.namemapping.get(x, x))
        df[self.config.key_column] = mapped
        return df
    
    def _get_unmapped_name(self):
        mapped_names = self.df_namemaps[self.namemap_key]
        df = self.df_op.drop_duplecate(self.config.key_column)
        df_unmapped = df[~df[self.config.key_column].isin(mapped_names), self.config.key_column].dropna()
        return df_unmapped.values
    
    def get_remain(self, df_op=None, aggset=None, to_html=True, **to_html_kwargs):
        df_op = df_op or self.df_op
        aggset = aggset or {ROW_COUNTER: sum, REMAIN_AMOUNT_COLUMN_NAME: sum}
        df = pd.merge(df_op, self.df_base, left_on=self.config.key_column, right_on=self.namemap_key)
        def get_remain_order(value):
            if value < 0:
                value = np.abs(value)
                return -get_remain_order(value)
            return np.ceil(value) - value
        df[REMAIN_ORDER_COLUMN_NAME] = df[self.config.order_amt_column].apply(get_remain_order)
        df[REMAIN_AMOUNT_COLUMN_NAME] = df[REMAIN_ORDER_COLUMN_NAME] * df[self.narcotic_amt]
        df[REMAIN_AMOUNT_UNIT_COLUMN_NAME] = df[self.narcotic_unit]
        df[ROW_COUNTER] = np.where(df[self.config.order_amt_column]>=0, 1, -1)
        initial_columns = [
            self.config.key_column, self.config.order_amt_column,
            REMAIN_ORDER_COLUMN_NAME, REMAIN_AMOUNT_COLUMN_NAME, REMAIN_AMOUNT_UNIT_COLUMN_NAME
        ]
        total_columns = list(OrderedDict.fromkeys(self._validate_extra_columns(self.config_extra_columns) + initial_columns))
        df = df.loc[df[REMAIN_AMOUNT_COLUMN_NAME]>0]
        df[self.config.key_column] = df[self.narcotic_key]

        grp = df.groupby([self.config.key_column, REMAIN_AMOUNT_UNIT_COLUMN_NAME]).agg(aggset)
        grp = grp.reset_index()
        grp_total_columns = [self.config.key_column, ROW_COUNTER, REMAIN_AMOUNT_COLUMN_NAME, REMAIN_AMOUNT_UNIT_COLUMN_NAME]
        df, grp = df[total_columns], grp[grp_total_columns]

        if to_html:
            return mark_safe(df.to_html(**to_html_kwargs)), mark_safe(grp.to_html(**to_html_kwargs))
        return df, grp

            

    
    def get_list(self):
        extra_columns = self._validate_extra_columns()
        not_null_columns = list(filter(lambda x: x in self.df_op.columns, csv2array(self.config.not_null_columns))) 
        order_by = list(filter(lambda x: x in self.df_op.columns, csv2array(self.config.orderby_columns))) 

        df = self._get_mapped_op()
        for col in not_null_columns:
            df = df.loc[df[col].notnull()]
        df = df.sort_values(order_by)
        return df[extra_columns]
    







    