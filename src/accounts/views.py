from django.shortcuts import render

from django.views.generic import CreateView
from django.contrib.auth.forms import UserCreationForm

class UserRegisterView(CreateView):
    template_name = 'registration/register.html'    
    form_class = UserCreationForm
    success_url = '/'

