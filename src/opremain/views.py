from django.shortcuts import render, redirect, reverse
from django.views.generic import *
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import F, Value, IntegerField, Count, Q

from .models import Narcotic, Config, NameMap, NarcoticUseFile
from .forms import ExcelFileAcceptForm, ConfigForm, CurrentNameFormSet, current_name_forset_builder, NameMapInlineFormset, NarcoticUseFileForm
from .services.core import OpremainDataFrame
from utils.mixins import ObjectListMixin


class ExcelFormView(FormView):
    form_class = ExcelFileAcceptForm
    template_name = 'opremain/excel_submit.html'
    success_url = '.'

    def get_context_data(self, **kwargs):
        context = super(ExcelFormView, self).get_context_data(**kwargs)
        context['object_list'] = self.request.user.config_set.all()
        return context
    
    def form_valid(self, form):
        excel = form.cleaned_data['excel']
        config = self.request.user.config_set.filter(activated=True).first()
        odf = OpremainDataFrame(Narcotic, config, excel)
        new_name_list = odf.get_new_names()
        for name in new_name_list:
            obj, created = NameMap.objects.get_or_create(current_name=name, 
                defaults={'config': config}
            )
            if created:
                obj.mapping_to = odf.find_similar_name_narcotics(name).first()
                obj.save()
        q = Q(current_name__isnull=True) & Q(excepted=False) | Q(activated=False)
        invalid_namemap_set = config.namemap_set.filter(q)
        if invalid_namemap_set.exists():  
            qs = config.namemap_set.filter(activated=False).order_by('-mapping_to')
            formset = NameMapInlineFormset(instance=config, queryset=qs)
            context = {
                'config': config, 'object': config,
                'formset': formset,
            }
            return render(self.request, 'opremain/mapping.html', context)
        
        kwargs = {'index': False, 'na_rep': "", 'classes': ['table', 'table-sm']}
        opremain_list, opremain_groupped = odf.get_remain_list(**kwargs)
        context = {
            'opremain_list': opremain_list,
            'opremain_groupped': opremain_groupped
        }
        return render(self.request, 'opremain/result.html', context)


    
def save_mapping(request, config_pk):
    if request.method == "POST":
        config = Config.objects.get(pk=config_pk)
        formset = NameMapInlineFormset(request.POST, instance=config)
        if formset.is_valid():
            formset.save()
        return redirect(reverse('opremain:excel-submit'))

