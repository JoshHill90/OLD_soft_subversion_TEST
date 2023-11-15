from django.contrib import admin
from django.urls import path
from .views import *
from . import views

urlpatterns = [
  path('o-panel/', views.o_client, name='o-client'),
  path('o-panel/invite', InviteView.as_view(), name='invite'),
  
  path('o-panel/binder/project/', views.project_main, name='o-project'),
  path('o-panel/binder/project/<slug:slug>', views.project_details, name='o-project-details'),
  
  path('o-panel/binder/project/events/<int:year>/<str:month>', views.clandar, name='project-calendar'),
  path('o-panel/binder/project/events/new', views.clandar, name='new-event'),
  path('o-panel/binder/project/<int:id>/notes',views.project_notes , name='project-notes'),
  
  path('o-panel/binder/project/requests/', views.project_request, name='o-reqeust'),
  path('o-panel/binder/project/requests/<slug:slug>', views.project_request_details, name='request-details'),
  path('o-panel/binder/project/request/approval/<slug:slug>', views.request_approval, name='request-approval'),

  path('c-panel/binder/<int:id>', views.c_panel, name='c-panel'),
  path('c-panel/binder/new-request', ClienRequestCreate.as_view(), name='project-request'),
  path('c-panel/binder/requests/<slug:slug>',views.request_status, name='request-status'),
  path('c-panel/binder/project/<slug:slug>/',views.client_project_details, name='c-project-details'),
]   
  
