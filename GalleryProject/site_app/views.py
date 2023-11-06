from typing import Any
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.views.generic.edit import FormView
from django.db.models import Q
from django.conf import settings
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Contact
from gallery.models import Image
from client.models import Project, Client
from .forms import ContactForm
from GalleryProject.env.app_Logic.smtp.MailerDJ import AutoReply
from GalleryProject.env.cloudflare_API.CFAPI import APICall

from pathlib import Path
import os
from dotenv import load_dotenv
from GalleryProject.env.app_Logic.json_utils import DataSetUpdate
from GalleryProject.env.app_Logic.smtp.MailerDJ import AutoReply
from GalleryProject.env.app_Logic.untility.quick_tools import QuickStripe, DateFunction, Hexer
from log_app.logging_config import logging
import time
from GalleryProject.env.cloudflare_API.CFAPI import APICall, Encode_Metadata


cf_api_call= APICall()
encode = Encode_Metadata()
qs = QuickStripe()
df = DateFunction()
hexer = Hexer()
smtp_request = AutoReply
dataQ = DataSetUpdate()

#-----------------------------------------------------------------------------------------------------------#
#
# functions
#
#-----------------------------------------------------------------------------------------------------------#


def append_cloundflare_id(cf_id, image_id, type_image):
    update_image_record = Image.objects.get(id=image_id)
    
    image_url = 'https://imagedelivery.net/4_y5kVkw2ENjgzV454LjcQ/' + cf_id +'/display'
    update_image_record.image_link = image_url
    update_image_record.save()


#-------------------------------------------------------------------------------------------------------#
# index - booking - galler - about 
#-------------------------------------------------------------------------------------------------------#


def index_page(request):
    image_list = Image.objects.filter(display='home')[:20]
    #cf_api_call.mass_import()
    return render(request, 'index.html', { 'image_list': image_list})

def about_page(request):
    return render(request, 'about.html')

def social_page(request):
    return render(request, 'social.html')

class ContactView(FormView):
    model = Contact
    template_name = 'contact.html'
    form_class = ContactForm
    
    def form_valid(self, form):
        self.object = form.save()
        name = self.object.name
        email = self.object.email
        subject = self.object.subject
        body = self.object.body

        smtp_request.contact_request(email, name)
        smtp_request.contact_alart(email, name, subject, body)

        return render(self.request, 'success/contact-success.html', {
            'name': name, 
            'email': email,
            'subject': subject,
        })
    
class ContactSuccess(TemplateView):
    template_name = 'success/contact-success.html'
    
class BackendIssue(TemplateView):
    template_name = 'error_page/issue.html'
    
#-------------------------------------------------------------------------------------------------------#
# owner panel main branch
#-------------------------------------------------------------------------------------------------------#

def o_main(request):
    image_list = Image.objects.all()
    project_list = Project.objects.all()
    client_list = Client.objects.all()
    gal1 = Image.objects.filter(Q(display="subgal1") | Q(display="gallery1"))
    gal2 = Image.objects.filter(Q(display="subgal2") | Q(display="gallery2"))
    gal4 = Image.objects.filter(Q(display="subgal4") | Q(display="gallery4"))
    site_image = Image.objects.filter(Q(client_id="1"))
    client_images = Image.objects.exclude(Q(client_id="1"))
    dataQ.json_chart_data()

    return render(request, 'o_panel/main.html', {
        'image_list': image_list,
        'project_list': project_list,
        'client_list': client_list,
        'gal1': gal1,
        'gal2': gal2,
        'gal4': gal4,
        'site_image': site_image,
        'client_images':client_images,
    })
    
def o_binder(request):
    
    project_list = Project.objects.all()
    client_list = Client.objects.all()
    image_list = Image.objects.all()
    
    return render(request, 'o_panel/binder.html', {
        'image_list': image_list,
        'project_list': project_list,
        'client_list': client_list
    })
    
def image_upload(request):

    multi_encode_bond = encode.direct_request_encoder()
    cloudflare_id = cf_api_call.auth_direct_upload(multi_encode_bond)
    cloudflare_id = str(cloudflare_id)
    front_end_url = f'https://upload.imagedelivery.net/4_y5kVkw2ENjgzV454LjcQ/{cloudflare_id}'

    return render(request, 'o_panel/image_upload.html',
                  {
                      'front_end_url': front_end_url,
                      'clfr_id': cloudflare_id}
                  )
    
def marketing(request):
    return render(request, 'o_panel/marketing.html')

def o_gallery(request):
    return render(request, 'o_panel/gallery.html')