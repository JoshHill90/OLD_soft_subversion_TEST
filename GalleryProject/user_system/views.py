from typing import Any
from django.forms.models import BaseModelForm 
from django.http import HttpResponse, JsonResponse
from django.views import generic
from django.views.generic import CreateView, ListView, DeleteView, DetailView, UpdateView
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy
from django.db.models import Q
from django.conf import settings

from log_app.logging_config import logging
from client.models import Client, Invite, Project, ProjectEvents
from .forms import RegForm, ProfileForm, LoginForm, InvoiceForm, LineItemForm
from .models import Invoice, LineItem
from gallery.models import Image
import stripe
from pathlib import Path
import os
from dotenv import load_dotenv
from GalleryProject.env.app_Logic.json_utils import DataSetUpdate
from GalleryProject.env.app_Logic.smtp.MailerDJ import AutoReply
from GalleryProject.env.app_Logic.untility.quick_tools import QuickStripe, DateFunction, Hexer
from log_app.logging_config import logging
import time


qs = QuickStripe()
df = DateFunction()
hexer = Hexer()
smtp_request = AutoReply

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
    client_list = Client.objects.all()
    image_list = Image.objects.all()
    invoice_info = Invoice.objects.all()
    project_list = Project.objects.exclude(name="Soft Subversion")
    project_invoice = ['']
    project_invoice.clear()
    bal_due = 0
    bal_paid = 0
    bal_ern = 0
    bal_out = 0
    # Get query parameters
    project_query = request.GET.get('project')
    client_query = request.GET.get('client')
    number_query = request.GET.get('number')
    completed_query = request.GET.get('fufiled')
    order_set = request.GET.get('order')
    


    # Calculate balances
    bills = Invoice.objects.all()
    for bill in bills:
        if not bill.fufiled:
            bal_due += bill.billed
            bal_paid += bill.paid
            bal_out = bal_due - bal_paid
        else:
            bal_ern += bill.paid
            bal_paid += bill.paid
    
    Invoice_totals = {
        'totalDue': bal_due,
        'totalPaid': bal_paid,
        'totalEarned': bal_ern,
        'outstanding': bal_out,
        }


    # Initial query set
    invoice_info = Invoice.objects.all()

    # Apply filters
    if project_query:
        invoice_info = invoice_info.filter(project_id__name=project_query)

    if client_query:
        invoice_info = invoice_info.filter(project_id__client_id__name=client_query)

    if number_query:
        invoice_info = invoice_info.filter(invoice__icontains=number_query)

    # Apply completion status filter
    if completed_query == 'open':
        invoice_info = invoice_info.filter(status='open')
    elif completed_query == 'paid':
        invoice_info = invoice_info.filter(status='paid')
    elif completed_query == 'draft':
        invoice_info = invoice_info.filter(status='draft')
    elif completed_query == 'void':
        invoice_info = invoice_info.filter(status='void')
        
    if order_set == 'Oldest':
        invoice_info = invoice_info.order_by('id')
    else:
        invoice_info = invoice_info.order_by('-id')
        
    # Invoice details set  
    for bill in invoice_info:
        client_billed = str(bill.project_id.client_id)    
        for project in project_list:
            if project.id == bill.project_id.id:
                project_images = []
                for image in image_list:
                    if image.project_id == project:
                        image_set = {'imageID': image.id, 'ImageTitle': image.title}
                        project_images.append(image_set)
                project_details = {
                    "project": project.name, 
                    'invoice': bill.invoice_id,
                    'billed': bill.billed,
                    'paid': bill.paid,
                    'status': bill.status,
                    'client': client_billed,
                    'images': project_images,
                                }
                project_invoice.append({'billID': bill.id, 'project_details': project_details})


    return render(
        request, 'o_panel/billing/billing.html', 
        {
            'invoice': project_invoice,
            'billing_totals':Invoice_totals,
            'project_list': project_list,
            'client_list': client_list
            }
        )        
    
def create_invoice(request):
    try:
        template_name = 'o_panel/billing/create-invoice.html'
        form_class = InvoiceForm
        project_list = Project.objects.exclude(name='Soft Subversion')
        model = Invoice
        invoice_details = {}
        line_items_cost = {}
        line_items_receipt = {}
        invoice_total = 0
        if request.method == 'POST':
            terms_form = request.POST
        
            if terms_form:
                #lambda converter 
                converted_to_cents = lambda dollar_amount: int(
                    str(
                        '{:.2f}'.format(
                            float(dollar_amount))).replace('.','')
                )
                # pulls request data from the from submitted and creates dicts 
                for key, value in zip(request.POST.keys(), request.POST.values()):
                    if 'line_item_cost' in key:
                        line_items_cost['C' + key[-1]] = value
                        invoice_total += float(value)
                        
                    elif 'line_item_receipt' in key:
                        line_items_receipt['R' + key[-1]] = value
                    else:
                        invoice_details[key] = value

                
                        
                # sets vars for frrom data
                
                selected_project = project_list.get(id=invoice_details.get('project_id'))
                stripe_date = df.date_distance(invoice_details.get('due_date'))
                set_payment_type = invoice_details.get('payment_type')
                set_details = f"{set_payment_type} for photography project:{selected_project.name}"
                
                # Get strip ID from client            
                stripe_id = selected_project.client_id.strip_id
                
                # strip invoice and project billing 
                set_invoice = qs.create_stripe_invoice(stripe_id, stripe_date, set_details)
                new_billing = model.objects.create(
                        project_id=selected_project,
                        invoice_id=set_invoice.id,
                        billed = invoice_total,
                        details=set_details,
                        due_date=df.number_to_days(stripe_date),
                        payment_type=set_payment_type
                )
                # checks for and creates line item and billing payments 
                if line_items_cost:
                    for cost, receipt in zip(line_items_cost.values(), line_items_receipt.values()):
                        
                        stripe_cost = converted_to_cents(cost)
                        set_lineitem = qs.create_stripe_line_item(stripe_cost, receipt, set_invoice, stripe_id)
                        LineItem.objects.create(
                            billing_id=new_billing,
                            amount=cost,
                            receipt=receipt,
                            time_stamp=df.date_now(),
                            item_id=set_lineitem.id,
                        )

                        time.sleep(5)
                
                if invoice_details.get('open'):
                    payment_link, invoice_update = qs.send_stripe_invoice(set_invoice.id)
                    new_billing.payment_link = payment_link
                    new_billing.status = invoice_update.status
                    new_billing.save()
                    ProjectEvents.objects.create(
                        title='Deposit Reminder',
                        project_id=selected_project,
                        billing_id=new_billing,
                        date=new_billing.due_date,
                        start=df.payment_time(),
                        end=df.payment_time(),
                        event_type='Payment Reminder',
                        details=f'Event for deposit reminder for project{selected_project}'
                    )

                if invoice_details.get('paidCash'):
                    invoice_update = qs.stripe_cash_payment(set_invoice.id)
                    new_billing.status = invoice_update.status
                    new_billing.paid = invoice_total
                    new_billing.fufiled = True
                    new_billing.save()

                return redirect('billing-details', new_billing.id)
            
        return render(request, template_name, {
            'form_class': form_class,
            'project_list': project_list,
            'model': model
        })
            
    except Exception as e:
        logging.error("Stripe invoice create operation failed: %s", str(e))
        return redirect('issue-backend', e=str(e))
