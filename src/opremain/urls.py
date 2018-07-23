from django.urls import path

from .views import *

app_name = 'opremain'

urlpatterns = [
    path('', ExcelFormView.as_view(), name='excel-submit'),
    path('mapping/<int:config_pk>/', save_mapping, name='mapping'),
    # path('', NarcoticUseFileCreateView.as_view(), name='narcotic-file-sumbit'),
    # path('config/', ConfigListView.as_view(), name='config-list'),
    # path('config/total/', ConfigTotalListView.as_view(), name='config-list-total'),
    # path('config/<int:pk>/', ConfigDetailView.as_view(), name='config-detail'),
    # path('config/update/<int:pk>/', ConfigUpdateView.as_view(), name='config-update'),
    # path('config/create/', ConfigCreateView.as_view(), name='config-create'),
    # path('config/<int:pk>/mapping/', NarcoticUseExcelSubmitView.as_view(), name='mapping-list'),
]
