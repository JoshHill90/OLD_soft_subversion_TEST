from typing import Any
from django.forms.models import BaseModelForm 
from django.http import HttpResponseRedirect, JsonResponse
from django.views.generic import CreateView, ListView, DeleteView, DetailView, UpdateView
from django.shortcuts import render, redirect 
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse 
from django.db.models import Q
from django.conf import settings
from .forms import ImageForms
from .models import Image, Dispaly, Tag
from client.models import Client, Project
from django.core.paginator import Paginator
from GalleryProject.env.app_Logic.photo_layer import col3_col6_col3
from GalleryProject.env.app_Logic.untility.quick_tools import ViewExtendedFunctions
from GalleryProject.env.cloudflare_API.CFAPI import APICall, Encode_Metadata
from log_app.logging_config import logging
import json
import re
from django.core import serializers
import time
from django.utils.text import slugify
import zlib
import requests
cf_api_call= APICall()
vef = ViewExtendedFunctions()
encodeM = Encode_Metadata()

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

	image_list1, image_list2, image_list3 = col3_col6_col3(image_inline)
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
		'image1': image1,
		'image2': image2,
		'image3': image3,
	})

def site_gallery(request, gal, subgal):
	image_list = Image.objects.filter(display=subgal)
	image_col1, image_col2, image_col3, new_list, len1, len2 = column_sort(image_list)
	header_image = image_list.get(display=gal)
	print(header_image, 'header')
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
	
def manage_gallery(request, gal, subgal):
    # The gallery management section empowers users to curate the content for various galleries, 
    # including the home page and header images for each gallery. 
    
	try:
		all_headers = (request.META)['HTTP_REFERER']	
		str_headers = str(all_headers)

		all_images = Image.objects.all().distinct()
		
		display = Dispaly.objects.all()
		
		subgal_instance = display.get(id=subgal)
		gall_instance = display.get(id=gal)
		get_gallery = all_images.filter(display=subgal)
		
		tag_query = request.GET.get('tags')
		project_query = request.GET.get('project')
		client_query = request.GET.get('client')
		order_set = request.GET.get('order')
		current_query = request.GET.get('current')
		
	
		p_q_check1 = str_headers.find('project=')
		p_q_check2 = str_headers.find('&', p_q_check1)
		c_q_check1 = str_headers.find('client=')
		c_q_check2 = str_headers.find('&', c_q_check1)
		t_q_check1 = str_headers.find('tags=')
		t_q_check2 = str_headers.find('&', t_q_check1)
		g_q_check1 = str_headers.find('current=')
		
		# Apply filters

		if project_query or len(str_headers[p_q_check1 :p_q_check2]) >= 8:
			#print('project')
			if project_query:
				all_images = all_images.filter(project_id__name__icontains=project_query)
			else:
				all_images = all_images.filter(project_id__name__icontains=str_headers[(p_q_check1 + 8):p_q_check2])

		if client_query or len(str_headers[c_q_check1 :c_q_check2]) >= 7:
			#print('client')
			if client_query:
				all_images = all_images.filter(
					Q(project_id__client_id__name__icontains=client_query) | 
					Q(project_id__client_id__user_id__first_name__icontains=client_query) |
					Q(project_id__client_id__user_id__last_name__icontains=client_query)
				)
			else:
				all_images = all_images.filter(
					Q(project_id__client_id__name__icontains=str_headers[(c_q_check1 + 7):c_q_check2]) | 
					Q(project_id__client_id__user_id__first_name__icontains=str_headers[(c_q_check1 + 7):c_q_check2]) |
					Q(project_id__client_id__user_id__last_name__icontains=str_headers[(c_q_check1 + 7):c_q_check2])
				)
	
		if tag_query or len(str_headers[t_q_check1 :t_q_check2]) >= 5:
			#print('tags')
			if tag_query:
				all_images = all_images.filter(tag__name__icontains=tag_query)
			else:
				all_images = all_images.filter(tag__name__icontains=str_headers[(t_q_check1 + 5):t_q_check2])
		
		#print('check 2', len(all_images))
		if current_query == 'True' or len(str_headers[g_q_check1:-1]) >= 10:
			print(subgal_instance.id)
			all_images = all_images.filter(display__id=subgal_instance.id)
		#print('check 3', len(all_images))
			
				
		if order_set == 'Oldest' or 'Oldest' in all_headers and order_set != 'Newest' :
			all_images = all_images.order_by('id')
			#print('older')
		else:
			all_images = all_images.order_by('-id')
			#print('newer')
		
		image_p = Paginator(all_images.all(), 21)
		last_page = image_p.num_pages
		page = request.GET.get('page')
		image_sets = image_p.get_page(page)
		next_image_set = []
		#print('check 4', len(all_images))
	
		# Post request section for functions called on the front
		if request.method == 'POST':
			
			# request to update the images of the current gallery
			# the images will only add images that are selected
			if 'update' in request.POST.values():
				#print('update')
				# creats blank image list and sets all images in the galllery to none
				image_listed = set()
				gal_image = all_images.filter(display__id=subgal)
				

				# creates keypair values for selected images
				for image_value, image_key in zip(request.POST.values(),  request.POST.keys()):
					if 'checkbox' in image_key:
						image_listed.add(image_value)
				# filter and update selected values
				
				selected_images = all_images.filter(id__in=image_listed)

				for image in selected_images:
					image.display.add(subgal_instance)

				return redirect('change-gal', gal=gal, subgal=subgal)

			# remove function: will only remove items selected
			elif 'remove' in request.POST.values():
				#print('remove')
				# creats blank image list and sets all images in the galllery to none
				image_listed = set()

				for image_value, image_key in zip(request.POST.values(),  request.POST.keys()):
					if 'checkbox' in image_key:
						image_listed.add(image_value)
		
				# filter for selected values
				selected_images = all_images.filter(id__in=image_listed)
				
				for image in selected_images:
					image.display.remove(subgal_instance)

				return redirect('change-gal', gal=gal, subgal=subgal)

			# removes all iamges from the gallery
			elif 'clearAll' in request.POST.values():
				#print('clearAll')
				gal_image = all_images.filter(Q(display__id=subgal) | Q(display__id=gal)).distinct()
				for image in gal_image:
					image.display.remove(subgal_instance)
					image.display.remove(gall_instance)

				return redirect('change-gal', gal=gal, subgal=subgal)
			
			# make image header for the gallery
			elif 'header' in request.POST.keys():

				header_image_id = request.POST.get('header')
				#print(header_image_id)
				header_image = all_images.filter(id=header_image_id)
				current_header = gall_instance.image_set.filter(display=gal)
				for image in current_header:
					image.display.remove(gal)
		
				header_image.get().display.add(gall_instance)
				return redirect('change-gal', gal=gal, subgal=subgal)

			# load more
			else:
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
						for tag_id in id_val:

							if tag_id['id'] == subgal_instance.id:
								image_display = subgal

					next_image_set.append({
						'id':image_id,
						'project':image_project, 
						'title':image_title, 
						'display':image_display,
						'image_link':image_link
						})
					
				return JsonResponse(next_image_set, safe=False)



		return render(request, 'o_panel/gallery/change-gallery.html', {
			'current_list': get_gallery,
			'gal': gal,
			'subgal':subgal,
			'image_sets':image_sets,
			'gal_name':gall_instance,
			'subgal_name':subgal_instance,
			'last_page':last_page
		})
	except Exception as e:
		logging.error("Gallery Control Error: %s", str(e))
		slugified_error_message = slugify(str(e))
		return redirect('issue-backend', status=500, error_message=slugified_error_message)
#-------------------------------------------------------------------------------------------------------#
# Image views
#-------------------------------------------------------------------------------------------------------#

def all_image_list(request):
	all_images = Image.objects.all().distinct()
	template_name = 'o_panel/images/image-details.html'
	all_headers = (request.META)['HTTP_REFERER']	
	str_headers = str(all_headers)
	
	tag_query = request.GET.get('tags')
	project_query = request.GET.get('project')
	client_query = request.GET.get('client')
	order_set = request.GET.get('order')
 
	p_q_check1 = str_headers.find('project=')
	p_q_check2 = str_headers.find('&', p_q_check1)
	c_q_check1 = str_headers.find('client=')
	c_q_check2 = str_headers.find('&', c_q_check1)
	t_q_check1 = str_headers.find('tags=')
	t_q_check2 = str_headers.find('&', t_q_check1)
	# Apply filters

	if project_query or len(str_headers[p_q_check1 :p_q_check2]) >= 8:
		if project_query:
			all_images = all_images.filter(project_id__name__icontains=project_query)
		else:
			all_images = all_images.filter(project_id__name__icontains=str_headers[(p_q_check1 + 8):p_q_check2])

	if client_query or len(str_headers[c_q_check1 :c_q_check2]) >= 7:
		if client_query:
			all_images = all_images.filter(
				Q(project_id__client_id__name__icontains=client_query) | 
				Q(project_id__client_id__user_id__first_name__icontains=client_query) |
				Q(project_id__client_id__user_id__last_name__icontains=client_query)
	   		)
		else:
			all_images = all_images.filter(
				Q(project_id__client_id__name__icontains=str_headers[(c_q_check1 + 7):c_q_check2]) | 
				Q(project_id__client_id__user_id__first_name__icontains=str_headers[(c_q_check1 + 7):c_q_check2]) |
				Q(project_id__client_id__user_id__last_name__icontains=str_headers[(c_q_check1 + 7):c_q_check2])
			)
   
	if tag_query or len(str_headers[t_q_check1 :t_q_check2]) >= 5:
		if tag_query:
			all_images = all_images.filter(tag__name__icontains=tag_query)
		else:
			all_images = all_images.filter(tag__name__icontains=str_headers[(t_q_check1 + 5):t_q_check2])
		
			
	if order_set == 'Oldest' or 'Oldest' in all_headers and order_set != 'Newest' :
		all_images = all_images.order_by('id')
		print('older')
	else:
		all_images = all_images.order_by('-id')
		print('newer')
	
	image_p = Paginator(all_images.all(), 21)
	last_page = image_p.num_pages
	page = request.GET.get('page')
	image_sets = image_p.get_page(page)
	next_image_set = []
 
	if request.method == 'POST':
		if request.method == 'POST' and 'delete' in request.POST.keys():
			print('delete')
			image_object_list = []
			for image_value, image_key in zip(request.POST.values(),  request.POST.keys()):
				if 'checkbox' in image_key:
					image_object_list.append(all_images.get(id=image_value))
     
			delete_image = vef.delete_image_set(image_object_list)
			
			if delete_image == 'success':
				return redirect('image-details')	

			else:
				e = delete_image
				logging.error("Client Invite Error: %s", str((e)))
				slugified_error_message = slugify(str(e))
				return redirect('issue-backend', status=500, error_message=slugified_error_message)	
			
		else:
			print('load')
			next_p = json.load(request)['next_p'] 
			next_page = int(next_p)
			next_set = list(image_p.page(next_page).object_list.values())
			
			for image_info in next_set:
				get_info = all_images.get(id=image_info['id'])
				image_id = str(get_info.id)
				image_project = str(get_info.project_id.name)
				image_title = str(get_info.title)
				image_link = str(get_info.image_link)
				
				image_display = str(0)

				image_display = []
						
		
				next_image_set.append({
					'id':image_id,
					'project':image_project, 
					'title':image_title, 
					'display':image_display,
					'image_link':image_link
					})
			return JsonResponse(next_image_set, safe=False)
	return render(request, template_name, {'image_sets':image_sets, 'last_page': last_page })
	
def image_upload(request):

	if request.method == 'POST':
		post_data = []
		count_given = json.load(request)['file_count'] 
		for count in range(count_given):
			multi_encode_bond = encodeM.direct_request_encoder()
			cloudflare_id = cf_api_call.auth_direct_upload(multi_encode_bond)

			if 'error' not in cloudflare_id:
				cloudflare_id = str(cloudflare_id)
				front_end_url = f'https://upload.imagedelivery.net/4_y5kVkw2ENjgzV454LjcQ/{cloudflare_id}'
				time.sleep(.02)
				post_data.append({'key': count, 'cf_id': cloudflare_id, 'cf_url': front_end_url})

			else:
				e = cloudflare_id
				logging.error("Client Invite Error: %s", str((e)))
				slugified_error_message = slugify(str(e))
				return redirect('issue-backend', status=500, error_message=slugified_error_message)
	
		return JsonResponse(post_data, safe=False)

	return render(request, 'o_panel/images/image_upload.html')
	
def image_process(request):
	data_packet = []
	cfId_slug = ''
	if request.method == 'POST':
		for cf_object in json.load(request)['data'] :
			
			slug_id =' ' + str(cf_object)
			cfId_slug = cfId_slug + slug_id
		compressed_data = zlib.compress(cfId_slug.encode())
		data_packet = compressed_data.hex()
		
		image_form_url = reverse('image-form', args=[data_packet])
		return JsonResponse(str(image_form_url), safe=False)

	return JsonResponse({'error': 'Invalid request method'})

def image_form(request, data_packet):
	compressed_data = bytes.fromhex(data_packet)
	decompressed_data = zlib.decompress(compressed_data)
	list_data = decompressed_data.decode().split()
	tags_object = Tag.objects.all()
	display_objects = Dispaly.objects.all()
	project_objects = Project.objects.all()
	
	if request.method == 'POST':

		new_image_form = request.POST
		if new_image_form:

			new_title = new_image_form.get('title')
			new_tags = new_image_form.getlist('tag') 
			new_display = new_image_form.getlist('display')
			new_project_id = new_image_form.get('project_id')
			
			id_counter = 1
			project_inst = project_objects.get(id=new_project_id)
			new_client = project_inst.client_id

		for cf_id in list_data:

			title_str = str(new_title) + str(id_counter)
			image_url = f'https://imagedelivery.net/4_y5kVkw2ENjgzV454LjcQ/{cf_id}/display'
			
			if requests.get(url=image_url).ok:

				image_object = Image.objects.create(
					title=title_str,
					client_id=new_client,
					project_id=project_inst,
					image_link=image_url,
					cloudflare_id=cf_id
				)
				
				
				id_counter += 1
				for new_gal in new_display:
					image_object.display.add(new_gal)
					image_object.save()
		
				for new_tag in new_tags:
					
					q_new_tag = tags_object.filter(name=new_tag).first()

					if q_new_tag:
						image_object.tag.add(q_new_tag.id)
					else:
						image_object.tag.create(name=new_tag)
		
					image_object.save()
		
				meta_data = {                            
					'title': title_str,
					'tag': new_tags,
					'display': new_display,
					'client_id': new_client,
					'project_id': project_inst.id, 
					'silk_id': image_object.silk_id
				}
				update_image = cf_api_call.image_update(meta_data, cf_id)
				if update_image == 'success':
					pass
				else:
					e = update_image
					logging.error("Client Invite Error: %s", str((e)))
					slugified_error_message = slugify(str(e))
					return redirect('issue-backend', status=500, error_message=slugified_error_message)
		return redirect('image-details')
				
			
		

	return render(request, 'o_panel/images/image-create.html',
		{
			'display_objects': display_objects,
			'tags_object':tags_object,
			'project_objects':project_objects
	})
