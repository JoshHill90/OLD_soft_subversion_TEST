from typing import Any
from django.forms.models import BaseModelForm 
from django.http import HttpResponse, JsonResponse
from django.views import generic
from django.views.generic import CreateView, ListView, DeleteView, DetailView, UpdateView
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy
from django.db.models import Q, Avg, Sum
from django.conf import settings
from django.core.paginator import Paginator
from log_app.logging_config import logging
from client.models import Client, Invite, Project, ProjectEvents
from .forms import RegForm, ProfileForm, LoginForm, InvoiceForm, LineItemForm
from .models import Invoice, LineItem
from gallery.models import Image
import json
import stripe
from pathlib import Path
import os
from dotenv import load_dotenv
from GalleryProject.env.app_Logic.json_utils import DataSetUpdate
from GalleryProject.env.app_Logic.smtp.MailerDJ import AutoReply
from GalleryProject.env.app_Logic.untility.quick_tools import QuickStripe, DateFunction, Hexer, DocumentFunctions, ViewExtendedFunctions
from log_app.logging_config import logging
import time
from django.utils.text import slugify

qs = QuickStripe()
df = DateFunction()
hexer = Hexer()
smtp_request = AutoReply
docf = DocumentFunctions()
vef = ViewExtendedFunctions()
current_dir = Path(__file__).resolve().parent
ven = current_dir / "../.env"
load_dotenv(ven)
stripe.api_key = os.getenv("STRIPE_KEY")
#-------------------------------------------------------------------------------------------------------#
# Registration views
#-------------------------------------------------------------------------------------------------------#

class CustomPasswordChangeView(PasswordChangeView):
	form_class = PasswordChangeView
	template_name = 'registration/change-password.html'
	success_url = reverse_lazy('index')


class UserEditView(generic.UpdateView):
	form_class = ProfileForm
	template_name = 'registration/edit-profile.html'
	success_url = reverse_lazy('index')

	def get_object(self, *args):
		return self.request.user
	

class UserRegistrationView(generic.CreateView):

	form_class = RegForm
	template_name = 'registration/register.html'
	
	def form_valid(self, form):
		print('valid')
		username = form.cleaned_data.get('username')
		hex_key = form.cleaned_data.get('hexkey')
		email = form.cleaned_data.get('email')
		phone = form.cleaned_data.get('phone')
		address_1 = form.cleaned_data.get('address_1')
		address_2 = form.cleaned_data.get('address_2')
		city = form.cleaned_data.get('city')
		state = form.cleaned_data.get('state')
		zip_code = form.cleaned_data.get('zip_code')
		invite = Invite.objects.filter(hexkey=hex_key).first()
		if invite:

			user = form.save()
			user.groups.set('2')
			user.save()
			user_id = form.instance
			client = Client.objects.create(name=username, 
										   email=email, 
										   phone=phone, 
										   address_1=address_1,
										   address_2=address_2,
										   city=city,
										   state=state, 
										   zip_code=zip_code,
										   user_id=user_id
										   )
			
			client.save()
			invite.used = True
			invite.save()
			return redirect('login')
		else:
			print('test 0')
			form.add_error('hexkey', 'Invalid hexkey. Please enter a valid key.')
			return self.form_invalid(form)
		
		
	def form_invalid(self, form):
		# Here, you can access and print the errors associated with each form field.
		for field_name, errors in form.errors.items():
			for error in errors:
				print(f"Field: {field_name}, Error: {error}")

		# You can also choose to customize the error messages here if needed.
		# For example, you can add custom error messages based on the field name.

		# To display these errors in your template, you can pass them to the template context.
		# Create a dictionary of error messages for each field.
		errors_dict = {field_name: errors[0] for field_name, errors in form.errors.items()}
		return self.render_to_response(self.get_context_data(form=form, errors=errors_dict))

	

class UserLoginView(generic.CreateView):
	form_class = LoginForm
	template_name = 'registration/login.html'
	success_url = reverse_lazy('index')
	
	
#-------------------------------------------------------------------------------------------------------#
# Invoice views
#-------------------------------------------------------------------------------------------------------#

def billing_panel(request):
	invoice_list = Invoice.objects.all()
	current_invoce = invoice_list.exclude(Q(status='void') | Q(status='uncollectable') | Q(fufiled=True))
	line_items = Invoice.objects.all()
	bal_due = 0
	bal_paid = 0
	total_ytd = 0
	bal_out = 0
	set_number = 10
	# Get query parameters
	project_query = request.GET.get('project')
	client_query = request.GET.get('client')
	number_query = request.GET.get('number')
	completed_query = request.GET.get('fufiled')
	order_set = request.GET.get('order')
	if request.GET.get('set'):
		set_number = request.GET.get('set')
	
	# Calculate balances current balance and ytd earnings
	for bill in current_invoce:
	   
		bal_due += bill.billed
		bal_paid += bill.paid
		bal_out = bal_due - bal_paid
		current_year = df.year_now()
		ytd_filter = invoice_list.filter(open_date__year=current_year)
		
		
		bal_paid += bill.paid
	total_ytd = ytd_filter.aggregate(total_earnings=Sum('paid'))['total_earnings']
		
	
	billing_card = [
		{'type': 'Total Due', 'cost': bal_due},
		{'type': 'Total Paid', 'cost': bal_paid},
		{'type': 'Year to Date', 'cost': total_ytd},
		{'type': 'Outstanding', 'cost': bal_out},
	]

	# Apply filters
	if project_query:
		invoice_list = invoice_list.filter(project_id__name=project_query)

	if client_query:
		invoice_list = invoice_list.filter(project_id__client_id__name=client_query)

	if number_query:
		invoice_list = invoice_list.filter(invoice__icontains=number_query)

	# Apply completion status filter
	if completed_query == 'open':
		invoice_list = invoice_list.filter(status='open')
	elif completed_query == 'paid':
		invoice_list = invoice_list.filter(status='paid')
	elif completed_query == 'draft':
		invoice_list = invoice_list.filter(status='draft')
	elif completed_query == 'void':
		invoice_list = invoice_list.filter(status='void')
		
	if order_set == 'Oldest':
		invoice_list = invoice_list.order_by('id')
	else:
		invoice_list = invoice_list.order_by('-id')
		
	invoice_p = Paginator(invoice_list.all(), set_number)
	last_page = invoice_p.num_pages
	page = request.GET.get('page')
	invoice_sets = invoice_p.get_page(page)
	
	if request.method == 'POST' and 'send' in request.POST:
		invoice_id = request.POST.get('invoice_id')
		project = invoice_list.project_set.get(id=invoice_id)
		client = project.client_set.get(id=project.client_id)	
		project_terms = project.project_terms_set.get(project_id=project)
		pdf_path = docf.pdf_path_finder(project_terms.scope)
		operation = vef.open_draft_invoice(client, project, invoice_id, invoice_list, pdf_path)
		if operation == 'success':
			return redirect('o-billing')
		
		else:
			logging.error("Invoice operation failed: %s", operation)
			slugified_error_message = slugify(str(operation)) 
			return redirect('issue-backend', status=502, error_message=slugified_error_message)

	# Invoice: delete if in draft, void if it's open
	if request.method == 'POST' and 'deleteOrVoid' in request.POST:
		object_id = request.POST.get('object_id')
		invoice = invoice_list.get(id=object_id)
		operation = vef.delete_or_void_invoice(invoice)
		if operation == 'success':
			return redirect('o-billing')
		
		else:
			logging.error("Invoice operation failed: %s", operation)
			slugified_error_message = slugify(str(operation)) 
			return redirect('issue-backend', status=501, error_message=slugified_error_message)
		
	# Invoice: mark paid in cash   
	if request.method == 'POST' and 'cash' in request.POST:
		object_id = request.POST.get('object_id')
		invoice = invoice_list.get(id=object_id)
		operation = vef.invoice_paid_in_cash(invoice)
		if operation == 'success':
			if invoice.payment_type == 'deposit':
				project.status = 'open'
				project.save()
			return redirect('o-billing')
		
		else:
			logging.error("Invoice operation failed: %s", operation)
			slugified_error_message = slugify(str(operation)) 
			return redirect('issue-backend', status=508, error_message=slugified_error_message)



 
	if request.method == 'POST' and 'invoice':
		invoice_form = InvoiceForm(data=request.POST)
		
		# Invoice: create a new invoice and line items, with an event for the payment reminder    
		invoice_model = Invoice
		line_item_model = LineItem
		#invoice_form = InvoiceForm()
		event_model = ProjectEvents
		# setting up empty var
		invoice_details = {}
		line_items_cost = {}
		line_items_receipt = {}
		invoice_total = 0
  
		if invoice_form.is_valid():

			if invoice_form:
	
				# pull request data from the form submitted and push into dicts to hold the values
				for key, value in zip(request.POST.keys(), request.POST.values()):
					print(key, value)
					if 'line_item_cost' in key:
						line_items_cost['C' + key[-1]] = value
						invoice_total += float(value)
						
					elif 'line_item_receipt' in key:
						line_items_receipt['R' + key[-1]] = value
					else:
						invoice_details[key] = value
				operation = vef.new_invoice(
					invoice_model,
					project, 
					invoice_details, 
					invoice_total, 
					line_items_cost,
					line_items_receipt,
					line_item_model,
	 				event_model
				)

				if operation == 'success':
					return redirect('o-billing')
				
				else:
					logging.error("Invoice operation failed: %s", operation)
					slugified_error_message = slugify(str(operation)) 
					return redirect('issue-backend', status=508, error_message=slugified_error_message)

	return render(
		request, 'o_panel/billing/billing.html', 
		{
			'invoices': invoice_sets,
			'invoice_list':invoice_list,
			'billing_set':billing_card,
			'last_page': last_page,
			'line_items':line_items
			}
		)        
	
def billing_details(request, id):
	invoice = Invoice.objects.get(id=id)
	lineitem = LineItem.objects.filter(billing_id=invoice)
	
	return render(request, 'o_panel/billing/billing-details.html', {
		'invoice': invoice,
		'lineitem': lineitem
	})