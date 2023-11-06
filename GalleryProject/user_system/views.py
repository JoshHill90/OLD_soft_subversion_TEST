from typing import Any
from django.forms.models import BaseModelForm 
from django.http import HttpResponse, JsonResponse
from django.views import generic
from django.views.generic import CreateView, ListView, DeleteView, DetailView, UpdateView
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy
from django.db.models import Q
from django.conf import settings
from GalleryProject.env.app_Logic.json_utils import DataSetUpdate
from GalleryProject.env.app_Logic.smtp.MailerDJ import AutoReply
from GalleryProject.env.app_Logic.untility.quick_tools import QuickStripe, DateFunction, Hexer
from log_app.logging_config import logging
from client.models import Client, Invite
from .forms import RegForm, ProfileForm, LoginForm


hexer = Hexer()

#-------------------------------------------------------------------------------------------------------#
# Registration views
#-------------------------------------------------------------------------------------------------------#

class CustomPasswordChangeView(PasswordChangeView):
    form_class = PasswordChangeView
    template_name = 'registration/change-password.html'
    success_url = reverse_lazy('index')


class UserEditView(generic.UpdateView):
    form_class = ProfileForm
    template_name = 'registration/edit-profile.html'
    success_url = reverse_lazy('index')

    def get_object(self, *args):
        return self.request.user
    

class UserRegistrationView(generic.CreateView):

    form_class = RegForm
    template_name = 'registration/register.html'
    
    def form_valid(self, form):
        username = form.cleaned_data.get('username')
        hex_key = form.cleaned_data.get('hexkey')
        email = form.cleaned_data.get('email')
        phone = form.cleaned_data.get('phone')
        contact_method = form.cleaned_data.get('contact_method')
        address_1 = form.cleaned_data.get('address_1')
        address_2 = form.cleaned_data.get('address_2')
        city = form.cleaned_data.get('city')
        state = form.cleaned_data.get('state')
        zip_code = form.cleaned_data.get('zip_code')
        invite = Invite.objects.filter(hexkey=hex_key).first()
        if invite:

            user = form.save()
            user.groups.set('1')
            user.save()
            user_id = form.instance
            client = Client.objects.create(name=username, 
                                           email=email, 
                                           phone=phone, 
                                           contact_method=contact_method,
                                           address_1=address_1,
                                           address_2=address_2,
                                           city=city,
                                           state=state, 
                                           zip_code=zip_code,
                                           user_id=user_id
                                           )
            
            client.save()
            invite.used = True
            invite.save()
            return redirect('login')
        else:
            print('test 0')
            form.add_error('hexkey', 'Invalid hexkey. Please enter a valid key.')
            return self.form_invalid(form)

class UserLoginView(generic.CreateView):
    form_class = LoginForm
    template_name = 'registration/login.html'
    success_url = reverse_lazy('index')