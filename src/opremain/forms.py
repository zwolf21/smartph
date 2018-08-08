from pprint import pprint
from collections import OrderedDict

from django import forms
from django.forms import formset_factory
from django.forms.models import modelformset_factory, inlineformset_factory

from utils.excels import is_excel
from .models import Config, NameMap, Narcotic


class ExcelFileAcceptForm(forms.Form):
	excel = forms.FileField(label='마약류불출현황파일')

	def clean_excel(self):
		excel = self.cleaned_data.get('excel')
		if not is_excel(excel.name):
			raise forms.ValidationError('엑셀파일이 아닙니다')
		return excel


class ConfigForm(forms.ModelForm):
	"""Form definition for Config."""

	class Meta:
		model = Config
		fields = 'title', 'key_column', 'not_null_columns', 'order_amt_column', 'orderby_columns', 'extra_columns', 'activated',



	

NameMapInlineFormset = inlineformset_factory(Config, NameMap,
	fields = ['current_name', 'mapping_to', 'excepted', 'activated',],
	extra = 0
)
		
