from django.shortcuts import render
from django.views.generic import FormView

from .forms import ExcelFileAcceptForm

from .services.core import OpremainDataFrame

class NarcoticUseExcelFormView(FormView):
    template_name = 'opremain/file_accept.html'
    form_class = ExcelFileAcceptForm
    success_url = '.'

    def form_valid(self, form):
        excel = form.cleaned_data.get('excel')
        odf = OpremainDataFrame(self.request.user.config_set.first(), excel)
        kwargs = {'index': False, 'na_rep': "", 'classes': ['table', 'table-sm']}
        opremain_list, opremain_groupped = odf.get_remain(**kwargs)
        context = {
            'opremain_list': opremain_list,
            'opremain_groupped': opremain_groupped
        }
        return render(self.request, 'opremain/result.html', context)
        

    
