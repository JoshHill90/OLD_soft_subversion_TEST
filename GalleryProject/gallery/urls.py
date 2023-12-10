from django.contrib import admin
from django.urls import path
from .views import *
from . import views

urlpatterns = [

    path('gallery/<slug:gal>/<slug:subgal>', views.site_gallery, name='site-gall'),
    
    path('o-panel/change/<slug:gal>/<slug:subgal>/', views.manage_gallery, name='change-gal'),
    
    path('o-panel/image-upload', views.image_upload, name='image-upload'),
    path('image/process/', views.image_process, name='image-process'),
    path('image/form/<slug:data_packet>', views.image_form, name='image-form'),
    path('image/all/', views.all_image_list, name='image-details'),
]