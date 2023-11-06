from django.contrib import admin
from django.urls import path
from .views import *
from . import views

urlpatterns = [
    path('gallery-hall/', views.gallery_hall, name='gallery'),
    path('gallery/<slug:gal>/<slug:subgal>', views.site_gallery, name='site-gall'),
    
    path('o-panel/change/<slug:gal>/<slug:subgal>', views.manage_gallery, name='change-gal')
]