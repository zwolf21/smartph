from django.shortcuts import render
from django.views.generic import *
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Narcotic, Config, NameMap
from .forms import ExcelFileAcceptForm, ConfigForm
from .services.core import OpremainDataFrame
from utils.mixins import ObjectListMixin


class NarcoticUseExcelFormView(FormView):
    template_name = 'opremain/file_accept.html'
    form_class = ExcelFileAcceptForm
    success_url = '.'

    def form_valid(self, form):
        excel = form.cleaned_data.get('excel')
        config = self.request.user.config_set.filter(activated=True).first()
        odf = OpremainDataFrame(config, excel)
        kwargs = {'index': False, 'na_rep': "", 'classes': ['table', 'table-sm']}
        opremain_list, opremain_groupped = odf.get_remain(**kwargs)
        context = {
            'opremain_list': opremain_list,
            'opremain_groupped': opremain_groupped
        }
        return render(self.request, 'opremain/result.html', context)
        

class ConfigListView(LoginRequiredMixin, ListView):
    model = Config

    def get_queryset(self):
        queryset = super(ConfigListView, self).get_queryset()
        queryset = queryset.filter(user=self.request.user, activated=True)
        return queryset

class ConfigDetailView(LoginRequiredMixin, ObjectListMixin, DetailView):
    model = Config

class ConfigCreateView(LoginRequiredMixin, CreateView):
    model = Config
    form_class = ConfigForm
    success_url = reverse_lazy('opremain:config-list')

class ConfigUpdateView(LoginRequiredMixin, ObjectListMixin, UpdateView):
    model = Config

class ConfigDetailView(LoginRequiredMixin, DeleteView):
    model = Config