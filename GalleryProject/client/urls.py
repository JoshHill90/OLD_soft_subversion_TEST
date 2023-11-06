from django.contrib import admin
from django.urls import path
from .views import *
from . import views

urlpatterns = [
  path('o-panel/binder/', views.o_client, name='o-client'),
  path('o-panel/invite/', InviteView.as_view(), name='invite'),
  path('o-panel/request/', views.client_request, name='o-reqeust'),
  
  path('o-panel/binder/project', views.project_main, name='o-project'),
  path('o-panel/binder/project/<int:pk>/details', views.project_details, name='project-details'),
  
  path('o-panel/binder/project/events/<int:year>/<str:month>', views.clandar, name='project-calendar'),
  path('o-panel/binder/project/<int:id>/notes',views.project_notes , name='project-notes'),
]   
  
