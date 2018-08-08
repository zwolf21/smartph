from django.urls import path

from .views import *

app_name = 'opremain'

urlpatterns = [
    path('', ExcelFormView.as_view(), name='excel-submit'),
    path('mapping/<int:config_pk>/', save_mapping, name='mapping'),
    path('config/create/', ConfigCreateView.as_view(), name='config-create'),
    path('config/update/<int:pk>/', ConfigUpdateView.as_view(), name='config-update'),
]
