from django.urls import path

from .views import NarcoticUseExcelFormView

app_name = 'opremain'

urlpatterns = [
    path('', NarcoticUseExcelFormView.as_view(), name='excel-accept'),
]