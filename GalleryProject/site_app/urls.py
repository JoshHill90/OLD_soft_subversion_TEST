from django.contrib import admin
from django.urls import path
from .views import *
from . import views

urlpatterns = [
    path('', views.index_page, name='index'),
    path('about/', views.about_page, name='about'),
    path('social/', views.social_page, name='social'),
    path('contact/', ContactView.as_view(), name='contact'),
    path('contact/success', ContactSuccess.as_view(), name='contact-success'),      
    path('error/<int:status>/<slug:error_message>', views.error_logger, name='issue-backend'),     
    
    path('o-panel', views.o_main, name='o_panel'),
    path('o-panel/binder', views.o_binder, name='binder'),
    path('o-panel/marketing', views.marketing, name='marketing'),
    path('o-panel/gallery', views.o_gallery, name='o-gallery'),
    
    path('o-panel/settings/documents', views.document_settings, name='o-documents'),
]