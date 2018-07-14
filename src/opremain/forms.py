from django import forms
from pprint import pprint

from .models import Config

from utils.excels import is_excel



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
		fields = 'title', 'key_column', 'not_null_columns', 'order_amt_column', 'orderby_columns', 'extra_columns',
