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
from .models import Image

from GalleryProject.env.app_Logic.photo_layer import col3_col6_col3
from GalleryProject.env.cloudflare_API.CFAPI import APICall, Encode_Metadata


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
    image_list = Image.objects.filter(Q(display="model") | Q(display="wedding") | Q(display="family"))

    return render(request, 'main_gallery/gallery.html', {
        'image_list': image_list,
    })

def site_gallery(request, gal, subgal):
    image_list = Image.objects.filter(Q(display=subgal) | Q(display=gal))
    image_col1, image_col2, image_col3, new_list, len1, len2 = column_sort(image_list)
    if gal == 'model':
        return render(request, 'main_gallery/model-gallery.html', {
            'image_list': image_list,
            'image_col1': image_col1,
            'image_col2': image_col2,
            'image_col3': image_col3,
            'new_list': new_list,
            'len1': len1,
            'len2': len2,
        })
    elif gal == 'wedding':
        return render(request, 'main_gallery/wedding-gallery.html', {
            'image_list': image_list,
            'image_col1': image_col1,
            'image_col2': image_col2,
            'image_col3': image_col3,
            'new_list': new_list,
            'len1': len1,
            'len2': len2,
        })
    elif gal == 'family':
        return render(request, 'main_gallery/family-gallery.html', {
            'image_list': image_list,
            'image_col1': image_col1,
            'image_col2': image_col2,
            'image_col3': image_col3,
            'new_list': new_list,
            'len1': len1,
            'len2': len2,
        })
    
def manage_gallery(request, gal, subgal):
    all_images = Image.objects.all()
    current_list = all_images.filter(Q(display=gal) | Q(display=subgal))
    

    return render(request, 'o_panel/gallery/change-gallery.html', {
        'current_list': current_list,
        'all_images': all_images,
        'gal': gal
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
    