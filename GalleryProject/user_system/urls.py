from django.urls import path
from .views import *
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('edit_profile/', UserEditView.as_view(), name='edit-profile'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('<int:user_id>/change-password/', auth_views.PasswordChangeView.as_view(template_name='registration/change-password.html'),name='change-password'),

    path('o-panel/binder/invoice/', views.billing_panel, name='o-billing'),
    path('o-panel/binder/invoice/create', views.create_invoice, name='create-invoice'),
    path('o-panel/binder/invoice/<int:id>', views.billing_details, name='billing-details'),
    
    # 
    #path('c-panel/binder/invoice/<int:id>', views.client_billing_details, name='billing-details')
]