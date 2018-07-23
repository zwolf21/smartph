from pprint import pprint
from collections import OrderedDict

from django import forms
from django.forms import formset_factory
from django.forms.models import modelformset_factory, inlineformset_factory

from utils.excels import is_excel
from .models import Config, NameMap, Narcotic, NarcoticUseFile

class NarcoticUseFileForm(forms.ModelForm):

	class Meta:
		model = NarcoticUseFile
		fields = 'excel',
	
	def clean_excel(self):
		excel = self.cleaned_data.get('excel')
		if not is_excel(excel.name):
			raise forms.ValidationError('엑셀파일이 아닙니다')
		return excel

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


class CurrentNameForm(forms.Form):
	current_name = forms.CharField(label='사용중인이름', required=False, disabled=True)
	mapping_to = forms.CharField(label='통합명칭', required=False)
	find_select = forms.MultipleChoiceField(choices=[('aaa', 'aaa')], widget=forms.RadioSelect())

	# def __init__(self, find_select=None, *args, **kwargs):
	# 	super().__init__(*args, **kwargs)
	# 	choices = Narcotic.objects.all().values_list('narcotic_name', 'narcotic_name')
	# 	self.fields['find_select'].choices = choices
	# 	self.fields['find_select'].initial = find_select

class NamemapForm(forms.ModelForm):
	find_select = forms.MultipleChoiceField(widget=forms.RadioSelect())

	class Meta:
		model = NameMap
		fields = 'current_name', 'mapping_to',
	
	# def __init__(self, *args, **kwargs):
	# 	super().__init__(*args, **kwargs)
	# 	# print(kwargs)
	# 	if choiceset is not None:
	# 		instance = kwargs['instance'].current_name
	# 		self.fields['find_select'].choices = choiceset.get(instance)

CurrentNameFormSet = formset_factory(CurrentNameForm, extra=0, max_num=200)

def current_name_forset_builder(name_list, odf):
	initials = [{'current_name': n} for n in name_list]
	choiceset = {}
	for name in name_list:
		val = odf.find_similar_name_narcotics(name)
		choiceset[name] = list(zip(val, val))
	# initials = list(sorted(initials, key=lambda e: len(choiceset[e])))
	NameMapFormSet = modelformset_factory(NameMap, NamemapForm, extra=len(initials))
	formset = NameMapFormSet(None, form_kwargs={'choiceset': choiceset})
	return formset
		
NameMapFormSet = modelformset_factory(NameMap, fields=['current_name', 'mapping_to'], form=NamemapForm)
NameMapInlineFormset = inlineformset_factory(Config, NameMap,
	fields = ['current_name', 'mapping_to', 'excepted', 'activated',],
	extra = 0
)
		

# def current_name_forset_builder(name_list, odf):
# 	initial = []
# 	for name in name_list:
# 		values = odf.find_similar_name_narcotics(name)
# 		record = {'current_name': name, 'find_select': list(zip(values, values))}
# 		initial.append(record)
# 	initial = list(sorted(initial, key=lambda row: len(row['find_select']), reverse=True))
# 	formset = formset_factory(CurrentNameForm, extra=0)(initial=initial)
# 	for form, rec in zip(formset, initial):
# 		name = rec['current_name']
# 		form.fields['find_select'].choices = rec['find_select']
# 	return formset