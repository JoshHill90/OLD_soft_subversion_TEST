from typing import Any
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.views.generic.edit import FormView
from django.db.models import Q
from django.conf import settings
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Contact, Document
from gallery.models import Image, Dispaly
from client.models import Project, Client
from .forms import ContactForm
from GalleryProject.env.app_Logic.smtp.MailerDJ import AutoReply
from GalleryProject.env.cloudflare_API.CFAPI import APICall
from GalleryProject.env.app_Logic.date_time_calendar import cal_gen, date_passed_check
import random
from pathlib import Path
import os
from dotenv import load_dotenv
from GalleryProject.env.app_Logic.json_utils import DataSetUpdate
from GalleryProject.env.app_Logic.smtp.MailerDJ import AutoReply
from GalleryProject.env.app_Logic.untility.quick_tools import QuickStripe, DateFunction, Hexer
from log_app.logging_config import logging
import time
from random import shuffle
from django.utils.text import slugify
qs = QuickStripe()
df = DateFunction()
hexer = Hexer()
smtp_request = AutoReply()
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
	all_images = Image.objects.all()
	image_list = Image.objects.filter(display=1)[:50]
	

	image1 = all_images.filter(display=3).first()

	image2 = all_images.filter(display=5).first()

	image3 = all_images.filter(display=7).first()

	return render(request, 'index.html', 
				  {
					'image_list': image_list,
					'image1':image1,
					'image2':image2,
					'image3':image3,
					})

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
		idN = self.object.pk

		email_sent = smtp_request.contact_request(email, name, subject)
		notice_sent = smtp_request.contact_alart(email, name, subject, body)
		if email_sent == 'success' and notice_sent == 'success':

			return redirect('contact-success', pk=idN)
		else:
			e = 'email-sent ', notice_sent, 'notice-sent ', notice_sent
			logging.error("Client Invite Error: %s", str((e)))
			slugified_error_message = slugify(str(e))
			return redirect('issue-backend', status=500, error_message=slugified_error_message)
	
class ContactSuccess(DetailView):
	model = Contact
	template_name = 'success/contact-success.html'
	
def error_logger(request, status, error_message):
	
	return render(request, 'error_page/issue.html', {'status': status, 'e': error_message})
	
#-------------------------------------------------------------------------------------------------------#
# owner panel main branch
#-------------------------------------------------------------------------------------------------------#

def o_main(request):
	image_list = Image.objects.all()
	project_list = Project.objects.all()
	client_list = Client.objects.all()
	gal1 = Image.objects.filter(Q(display=4) | Q(display=3))
	gal2 = Image.objects.filter(Q(display=5) | Q(display=7))
	gal4 = Image.objects.filter(Q(display=6) | Q(display=8))
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
	month0, month, month2, cal, year, todays_date, cal_date = cal_gen()
	project_list = Project.objects.all()
	client_list = Client.objects.all()
	image_list = Image.objects.all()
	
	return render(request, 'o_panel/binder.html', {
		'image_list': image_list,
		'project_list': project_list,
		'client_list': client_list,
		'year': year,
		'month':month,
	})
	

def marketing(request):
	return render(request, 'o_panel/marketing.html')

def o_gallery(request):
	return render(request, 'o_panel/gallery.html')


def document_settings(request):
	documents = Document.objects.filter(doc_type='site')