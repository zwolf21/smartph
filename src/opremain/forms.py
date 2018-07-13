from django import forms
from pprint import pprint

from utils.excels import is_excel


class ExcelFileAcceptForm(forms.Form):
	excel = forms.FileField(label='마약류불출현황파일')

	def clean_excel(self):
		excel = self.cleaned_data.get('excel')
		if not is_excel(excel.name):
			raise forms.ValidationError('엑셀파일이 아닙니다')
		return excel