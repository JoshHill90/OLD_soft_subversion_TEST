from typing import Any
from django.forms.models import BaseModelForm 
from django.http import HttpResponse, JsonResponse
from django.views import generic
from django.views.generic import CreateView, ListView, DeleteView, DetailView, UpdateView
from django.shortcuts import render
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy
from django.db.models import Q
from django.conf import settings
from .forms import ImageForms
from .models import Image

from GalleryProject.env.app_Logic.photo_layer import col3_col6_col3


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
    template_name = 'gallery/image/image-details.html'
    
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