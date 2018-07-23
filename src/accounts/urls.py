from django.urls import path, include

from django.views.generic import TemplateView
from django.contrib import admin

from .views import UserRegisterView

##TAG: 로그인urlconf, login url, 사용자 등록은 따로 구현해야함


app_name = 'accounts'

urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('register/', UserRegisterView.as_view(), name='register'),
]