from typing import Any
from django.forms.models import BaseModelForm 
from django.http import HttpResponse, JsonResponse
from django.views import generic
from django.views.generic import CreateView, ListView, DeleteView, DetailView, UpdateView
from django.shortcuts import render, redirect
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy
from django.db.models import Q
from django.conf import settings
from .forms import ImageForms
from .models import Image, Dispaly
from django.core.paginator import Paginator
from GalleryProject.env.app_Logic.photo_layer import col3_col6_col3
from GalleryProject.env.cloudflare_API.CFAPI import APICall, Encode_Metadata
import json
from django.core import serializers


cf_api_call= APICall()
encode = Encode_Metadata()

#-----------------------------------------------------------------------------------------------------------#
#
# functions
#
#-----------------------------------------------------------------------------------------------------------#
def append_cloundflare_id(cf_id, image_id):

	update_image_record = Image.objects.get(id=image_id)
	
	image_url = 'https://imagedelivery.net/4_y5kVkw2ENjgzV454LjcQ/' + cf_id +'/display'
	update_image_record.image_link = image_url
	update_image_record.save()
#-------------------------------------------------------------------------------------------------------#
# gallery column sorter
#-------------------------------------------------------------------------------------------------------#

def column_sort(image_list):
	image_inline = []
	image_col1 = []
	image_col2 = []
	image_col3 = []
	new_list = []

	for image in image_list:
		new_list = []
		image_inline.append([image.id, image.portrait_format])

	image_list1, image_list2, image_list3 = col3_col6_col3 (image_inline)
	for image in image_list:
		for image1 in image_list1:
			if image.id in image1:
				image_col1.append(image)
				
		for image2 in image_list2:
			if image.id in image2:
				image_col2.append(image)

		for image3 in image_list3:
			if image.id in image3:
				image_col3.append(image)

	len1 = len(image_col1)
	len2 = len(image_col2)+len1
	for listed_item in image_col1 + image_col2 + image_col3:
		new_list.append(listed_item)

	return image_col1, image_col2, image_col3, new_list, len1, len2

#-------------------------------------------------------------------------------------------------------#
# gallery views site, project and client
#-------------------------------------------------------------------------------------------------------#

def gallery_hall(request):
	#image_list = Image.objects.filter(Q(display__id=3) | Q(display=5) | Q(display=7))
	display1 = Dispaly.objects.get(id=3)
	image1 = display1.image_set.filter(display=3).first()
 
	display2 = Dispaly.objects.get(id=5)
	image2 = display2.image_set.filter(display=5).first()
 
	display3 = Dispaly.objects.get(id=7)
	image3 = display3.image_set.filter(display=7).first()
	print(image1, image2, image3)
 
	return render(request, 'main_gallery/gallery.html', {
		'image1': image3,
		'image2': image2,
		'image3': image1,
	})

def site_gallery(request, gal, subgal):
	image_list = Image.objects.filter(Q(display=subgal) | Q(display=gal))
	image_col1, image_col2, image_col3, new_list, len1, len2 = column_sort(image_list)
	display1 = Dispaly.objects.get(id=gal)
	header_image = display1.image_set.all()
	print(header_image)
	if gal == '3':
		return render(request, 'main_gallery/model-gallery.html', {
			'image_list': image_list,
			'image_col1': image_col1,
			'image_col2': image_col2,
			'image_col3': image_col3,
			'new_list': new_list,
			'len1': len1,
			'len2': len2,
			'header_image': header_image
		})
	elif gal == '5':
		return render(request, 'main_gallery/wedding-gallery.html', {
			'image_list': image_list,
			'image_col1': image_col1,
			'image_col2': image_col2,
			'image_col3': image_col3,
			'new_list': new_list,
			'len1': len1,
			'len2': len2,
   			'header_image': header_image
		})
	elif gal == '7':
		return render(request, 'main_gallery/family-gallery.html', {
			'image_list': image_list,
			'image_col1': image_col1,
			'image_col2': image_col2,
			'image_col3': image_col3,
			'new_list': new_list,
			'len1': len1,
			'len2': len2,
			'header_image': header_image
		})
	
def manage_gallery(request, gal, subgal, project=None):
	
	if project:
		all_images = Image.objects.filter(project)
	else:
		all_images = Image.objects.all()
  
	display = Dispaly.objects.all()
	subgal_instance = display.get(id=subgal)
	gall_instance = display.get(id=subgal)
	get_gallery = all_images.filter(Q(display=gal) | Q(display=subgal))
	
	project_query = request.GET.get('project')
	client_query = request.GET.get('client')
	order_set = request.GET.get('order')	
 
	# Apply filters
	if project_query:
		all_images = all_images.filter(Q(project_id__icontains=project_query))
	if client_query:
		all_images = all_images.filter(Q(project_id__client_id__name__icontains=client_query))
		
			
	if order_set == 'Oldest':
		all_images = all_images.order_by('id')
	else:
		all_images = all_images.order_by('-id')
	
	image_p = Paginator(all_images.all(), 20)
	last_page = image_p.num_pages
	page = request.GET.get('page')
	image_sets = image_p.get_page(page)
	next_image_set = []
 
	if request.method == 'POST' and 'update' in request.POST.values():
		print('update')
		print(request.POST.keys())
		# creats blank image list and sets all images in the galllery to none
		image_listed = set()
		gal_image = all_images.filter(Q(display__id=subgal) | Q(display__id=gal)).distinct()
		print(gal_image)
		for image in gal_image:
			image.display.remove(subgal)
		# creates keypair values for selected images
		for image_value, image_key in zip(request.POST.values(),  request.POST.keys()):
			if 'checkbox' in image_key:
				image_listed.add(image_value)
		# filter and update selected values
		
		selected_images = all_images.filter(id__in=image_listed)
		
		for image in selected_images:
			image.display.add(subgal_instance)

		return redirect('change-gal', gal=gal, subgal=subgal)
	
	if request.method == 'POST' and 'update' not in request.POST.keys() and 'header' not in request.POST.keys():
		next_p = json.load(request)['next_p'] 
		next_page = int(next_p)
		next_set = list(image_p.page(next_page).object_list.values())
		for image_info in next_set:
			get_info = all_images.get(id=image_info['id'])
			image_id = str(get_info.id)
			image_project = str(get_info.project_id.name)
			image_title = str(get_info.title)
			image_link = str(get_info.image_link)
			id_val = get_info.display.values()
			image_display = str(0)
			if id_val:
				id_display =id_val[0]

				if subgal_instance.id == id_display['id']:
					image_display = subgal
					
	
			next_image_set.append({
				'id':image_id,
				'project':image_project, 
				'title':image_title, 
				'display':image_display,
				'image_link':image_link
				})
			
		return JsonResponse(next_image_set, safe=False)

	if request.method == 'POST' and 'header' in request.POST.keys():

		header_image_id = request.POST.get('header')
		print(header_image_id)
		header_image = all_images.filter(id=header_image_id)
		current_header = gall_instance.image_set.filter()
		for image in current_header:
			image.display.remove(gal)
   
		header_image.get().display.add(gal)
		return redirect('change-gal', gal=gal, subgal=subgal)


	return render(request, 'o_panel/gallery/change-gallery.html', {
		'current_list': get_gallery,
		'gal': gal,
		'subgal':subgal,
		'image_sets':image_sets,
		'gal_name':gall_instance,
		'subgal_name':subgal_instance,
		'last_page':last_page
	})

#-------------------------------------------------------------------------------------------------------#
# Image views
#-------------------------------------------------------------------------------------------------------#

class ImageDetailView(DetailView):
	model = Image
	form_class = ImageForms
	template_name = 'o_panel/images/image-details.html'
	
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		current_pk = self.kwargs['pk']
		try:
			query_previous_image = Image.objects.filter(pk__lt=current_pk).order_by('-pk').first()
			previous_image = query_previous_image.id
		except AttributeError:
			previous_image = ''
		
		try:
			query_next_image = Image.objects.filter(pk__gt=current_pk).order_by('pk').first()
			next_image = query_next_image.id
		except AttributeError:
			next_image = ''

		context['previous_image'] = previous_image
		context['next_image'] = next_image
		
		return context
	
def image_upload(request):

	multi_encode_bond = encode.direct_request_encoder()
	cloudflare_id = cf_api_call.auth_direct_upload(multi_encode_bond)
	cloudflare_id = str(cloudflare_id)
	front_end_url = f'https://upload.imagedelivery.net/4_y5kVkw2ENjgzV454LjcQ/{cloudflare_id}'

	return render(request, 'o_panel/images/image_upload.html',
				  {
					  'front_end_url': front_end_url,
					  'clfr_id': cloudflare_id}
				  )
	
class CreateImage(CreateView):
	model = Image
	form_class = ImageForms
	template_name = 'o_panel/images/image-create.html'

	def form_valid(self, form):
		self.object = form.save()
		cf_id = form.cleaned_data.get('cloudflare_id',)
		image_id = self.object.id
		append_cloundflare_id(cf_id, image_id)
		title = form.cleaned_data.get('title', )
		tag = form.cleaned_data.get('tag', )
		private = form.cleaned_data.get('private', )
		display = form.cleaned_data.get('display', )
		aspect  = form.cleaned_data.get('aspect', )
		client_id  = form.cleaned_data.get('client_id', )
		client_id_str = str(client_id)
		project_id = form.cleaned_data.get('project_id', )
		project_id_str = str(project_id.name)
		silk_id = self.object.silk_id
		metadata_push = [
				title,  
				tag,
				private, 
				display, 
				aspect, 
				client_id_str, 
				project_id_str,
				cf_id,
				silk_id,
		]
		api = APICall()
		api.image_update(metadata_push, cf_id, self.type_image)
		return redirect('image-details', image_id)
	