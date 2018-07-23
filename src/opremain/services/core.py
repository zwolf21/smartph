import functools, operator, re
from collections import OrderedDict

from django.utils.safestring import mark_safe

from django_pandas.io import read_frame
import pandas as pd
import numpy as np

from utils.shortcuts import csv2array, classinit, findsim
from .name_ignore import IGNORE_NAME_PATTERNS


REMAIN_ORDER_COLUMN_NAME = '처방잔량'
REMAIN_AMOUNT_COLUMN_NAME = '단위잔량'
REMAIN_AMOUNT_UNIT_COLUMN_NAME = '단위'
REMAIN_AMOUNT_SUM_COLUMN_NAME = '잔량합계'
STANDARD_NARCOTIC_NAME = '표준약품명'
ROW_COUNTER = '앰플/바이알개수'
SHAPE_COLUMN_NAME = '규격'

NARCOTIC_LOOKUP_FIELDS = [
    'keyword', 'company_keyword', 'sub_keyword','full_amt_exp', 'amt_weight_exp', 'amt_volum_exp', 'pct_exp'
]
NARCOTIC_LIMIT = 5

@classinit({
    'namemap_key': 'current_name',
    'namemap_value': 'mapping_to',
    'namemap_excepted': 'excepted',
    'namemap_activated': 'activated',
    'narcotic_key': 'narcotic_name',
    'narcotic_amt_ml': 'amt_ml',
    'narcotic_amt_mg': 'amt_mg',
    'narcotic_unit': 'unit',
    'narcotic_shape': 'shape',
    'config_extra_columns': 'extra_columns'
})
class OpremainDataFrame(object):

    def __init__(self, Narcotic, config, excel):
        self.Narcotic = Narcotic
        self.config = config
        self.excel = pd.read_excel(excel, ignore_index=True)
        self.opremains = self.excel
        self.opremains_base_columns = self.opremains.columns
        
        for col in csv2array(self.config.not_null_columns, self.opremains_base_columns):
            self.opremains = self.opremains[self.opremains[col].notnull()]

        self.narcotics = read_frame(Narcotic.objects.all())
        # mapping_to 가 하나라도 null 이면 dataframe 에서 fk 인식못함
        self.namemaps = read_frame(self.config.namemap_set.filter(mapping_to__isnull=False))
        
        self.mappings = pd.merge(
            self.namemaps, self.narcotics, left_on=self.namemap_value, right_on=self.narcotic_key
        )
        self.opremains = pd.merge(
            self.opremains, self.mappings, left_on=self.config.key_column, right_on=self.namemap_key, how='left'
        )

    def get_unmapped_names(self):
        df = self.opremains
        df = df[df[self.namemap_value].isnull() | df[self.namemap_excepted]==False]
        return list(df[self.config.key_column].unique())
    
    def get_new_names(self):
        return list(self.opremains[self.config.key_column].unique())

    def find_similar_name_narcotics(self, name, ignore_name_patterns=IGNORE_NAME_PATTERNS, lookup_fields=NARCOTIC_LOOKUP_FIELDS, limit=NARCOTIC_LIMIT):
        name = name.lower()
        for ignpat in ignore_name_patterns:
            g = re.search(ignpat, name)
            if g:
                return self.Narcotic.objects.none()
        df = self.narcotics.copy()
        for f in lookup_fields:
            unique = df[df[f].notnull()][f].unique()
            for item in map(str.lower, unique):
                if item in name:
                    filtered = df[df[f]==item]
                    if filtered.shape[0] == 0:
                        break
                    else:
                        df = filtered
        if 0 < df.shape[0] < limit:
            df = df[:limit]
            qs = self.Narcotic.objects.filter(**{"{}__in".format(self.narcotic_key): df[self.narcotic_key]})
            return qs
        return self.Narcotic.objects.none()
    
    def get_remain_list(self, aggset=None, **to_html_kwargs):
        aggset = aggset or {ROW_COUNTER: sum, REMAIN_AMOUNT_COLUMN_NAME: sum}
        df = self.opremains
        nar_cur_nm = self.config.key_column
        nar_nm = self.narcotic_key
        ord_amt = self.config.order_amt_column
        unit_nm = self.narcotic_unit
        shape_nm = self.narcotic_shape
        amt_ml = self.narcotic_amt_ml
        amt_mg = self.narcotic_amt_mg
        extra_col = csv2array(self.config.extra_columns)
        order_cols = csv2array(self.config.orderby_columns)

        def get_remain_order(value):
            if value < 0:
                value = np.abs(value)
                return -get_remain_order(value)
            return np.ceil(value) - value
        
        df[REMAIN_ORDER_COLUMN_NAME] = df[ord_amt].apply(get_remain_order)
        df[REMAIN_AMOUNT_COLUMN_NAME] = df[REMAIN_ORDER_COLUMN_NAME] * np.where(df[amt_ml], df[amt_ml], df[amt_mg])
        df[REMAIN_AMOUNT_UNIT_COLUMN_NAME] = df[unit_nm]
        df[ROW_COUNTER] = np.where(df[ord_amt]>=0, 1, -1)

        initial_columns = [
            nar_cur_nm, ord_amt,
            REMAIN_ORDER_COLUMN_NAME, REMAIN_AMOUNT_COLUMN_NAME, REMAIN_AMOUNT_UNIT_COLUMN_NAME
        ]
        total_columns = list(OrderedDict.fromkeys(extra_col+initial_columns))
        df = df.loc[df[REMAIN_AMOUNT_COLUMN_NAME]>0]
        df[nar_cur_nm] = df[nar_nm]

        if order_cols:
            df = df.sort_values(order_cols)

        grp = df.groupby([nar_cur_nm, REMAIN_AMOUNT_UNIT_COLUMN_NAME, shape_nm]).agg(aggset)
        grp = grp.reset_index()
        grp_total_columns = [nar_cur_nm, ROW_COUNTER, shape_nm, REMAIN_AMOUNT_COLUMN_NAME, REMAIN_AMOUNT_UNIT_COLUMN_NAME]
        df, grp = df[total_columns], grp[grp_total_columns]
        grp = grp.rename(columns={shape_nm: SHAPE_COLUMN_NAME})
        return mark_safe(df.to_html(**to_html_kwargs)), mark_safe(grp.to_html(**to_html_kwargs))






# class OpremainDataFrame(object):

#     def __init__(self, config, excel_io):
#         namemaps = config.namemap_set.all()
#         if not namemaps:
#             raise ValueError('매칭된 품목이 하나도 없습니다.')

#         Narcotic = namemaps.first().mapping_to.__class__
#         self.config = config
#         self.df_namemaps = read_frame(namemaps)
#         self.df_op = pd.read_excel(excel_io, ignore_index=True)
#         self.namemapping = dict(self.df_namemaps.set_index(self.namemap_key)[self.namemap_value])
#         self.df_narcotic = read_frame(Narcotic.objects.all())
#         self.df_base = pd.merge(self.df_namemaps, self.df_narcotic, left_on=self.namemap_value, right_on=self.narcotic_key)

#     def _validate_extra_columns(self, attr_nm):
#         valid_columns = []
#         columns = csv2array(getattr(self.config, attr_nm))
#         for colnm in columns:
#             find_colnm = findsim(colnm, self.df_op.columns)
#             if find_colnm is not None:
#                 valid_columns.append(find_colnm)
#         return valid_columns
    
#     def _get_mapped_op(self):
#         df = self.df_op.copy()
#         mapped = df[self.config.key_column].apply(lambda x: self.namemapping.get(x, x))
#         df[self.config.key_column] = mapped
#         return df
    
#     def _get_unmapped_name(self):
#         mapped_names = self.df_namemaps[self.namemap_key]
#         df = self.df_op.drop_duplecate(self.config.key_column)
#         df_unmapped = df[~df[self.config.key_column].isin(mapped_names), self.config.key_column].dropna()
#         return df_unmapped.values
    
#     def get_remain(self, df_op=None, aggset=None, to_html=True, **to_html_kwargs):
#         df_op = df_op or self.df_op
#         aggset = aggset or {ROW_COUNTER: sum, REMAIN_AMOUNT_COLUMN_NAME: sum}
#         df = pd.merge(df_op, self.df_base, left_on=self.config.key_column, right_on=self.namemap_key)
        # def get_remain_order(value):
        #     if value < 0:
        #         value = np.abs(value)
        #         return -get_remain_order(value)
#             return np.ceil(value) - value
#         df[REMAIN_ORDER_COLUMN_NAME] = df[self.config.order_amt_column].apply(get_remain_order)
#         df[REMAIN_AMOUNT_COLUMN_NAME] = df[REMAIN_ORDER_COLUMN_NAME] * df[self.narcotic_amt]
#         df[REMAIN_AMOUNT_UNIT_COLUMN_NAME] = df[self.narcotic_unit]
#         df[ROW_COUNTER] = np.where(df[self.config.order_amt_column]>=0, 1, -1)
#         initial_columns = [
#             self.config.key_column, self.config.order_amt_column,
#             REMAIN_ORDER_COLUMN_NAME, REMAIN_AMOUNT_COLUMN_NAME, REMAIN_AMOUNT_UNIT_COLUMN_NAME
#         ]
#         total_columns = list(OrderedDict.fromkeys(self._validate_extra_columns(self.config_extra_columns) + initial_columns))
#         df = df.loc[df[REMAIN_AMOUNT_COLUMN_NAME]>0]
#         df[self.config.key_column] = df[self.narcotic_key]

#         grp = df.groupby([self.config.key_column, REMAIN_AMOUNT_UNIT_COLUMN_NAME]).agg(aggset)
#         grp = grp.reset_index()
#         grp_total_columns = [self.config.key_column, ROW_COUNTER, REMAIN_AMOUNT_COLUMN_NAME, REMAIN_AMOUNT_UNIT_COLUMN_NAME]
#         df, grp = df[total_columns], grp[grp_total_columns]

#         if to_html:
#             return mark_safe(df.to_html(**to_html_kwargs)), mark_safe(grp.to_html(**to_html_kwargs))
#         return df, grp

            

    
    # def get_list(self):
    #     extra_columns = self._validate_extra_columns()
    #     not_null_columns = list(filter(lambda x: x in self.df_op.columns, csv2array(self.config.not_null_columns))) 
    #     order_by = list(filter(lambda x: x in self.df_op.columns, csv2array(self.config.orderby_columns))) 

    #     df = self._get_mapped_op()
    #     for col in not_null_columns:
    #         df = df.loc[df[col].notnull()]
    #     df = df.sort_values(order_by)
    #     return df[extra_columns]
    







    