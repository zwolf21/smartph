from django.urls import path

from .views import *

app_name = 'opremain'

urlpatterns = [
    path('config/', ConfigListView.as_view(), name='config-list'),
    path('config/<int:pk>/', ConfigDetailView.as_view(), name='config-detail'),
    path('config/update/<int:pk>/', ConfigUpdateView.as_view(), name='config-update'),
    path('config/create/', ConfigCreateView.as_view(), name='config-create'),
    path('', NarcoticUseExcelFormView.as_view(), name='excel-accept'),
]