from django.contrib import admin
from django.urls import path
from .views import *
from . import views

urlpatterns = [
    path('gallery-hall/', views.gallery_hall, name='gallery'),
    path('gallery/<slug:gal>/<slug:subgal>', views.site_gallery, name='site-gall'),
    
    path('o-panel/change/<slug:gal>/<slug:subgal>/', views.manage_gallery, name='change-gal'),
    
    path('o-panel/image-upload', views.image_upload, name='image-upload'),
    path('image/create/<str:clfr_id>', CreateImage.as_view(), name='image-create'),
    path('image/<int:pk>/details', ImageDetailView.as_view(), name='image-details'),
]