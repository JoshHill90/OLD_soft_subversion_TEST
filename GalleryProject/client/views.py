from django.forms.models import BaseModelForm
from django.http import HttpResponse
from django.views.generic import CreateView, ListView, DeleteView, DetailView, UpdateView, TemplateView
from django.urls import reverse_lazy
from django.db.models import Q
from django.conf import settings
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from .forms import InviteForm, RequestReplyComment, ProjectRequestForm, ProjectTermsForm
from .models import Client, Invite, Project, ProjectRequest, RequestReply, ProjectTerms, ProjectEvents
from gallery.models import Image
from user_system.models import Invoice, LineItem
from django.utils.text import slugify
from GalleryProject.env.app_Logic.json_utils import DataSetUpdate
from log_app.logging_config import logging
from GalleryProject.env.app_Logic.smtp.MailerDJ import AutoReply
from GalleryProject.env.app_Logic.untility.quick_tools import QuickStripe, DateFunction, Hexer
from GalleryProject.env.app_Logic.date_time_calendar import cal_gen, date_passed_check

import calendar
import stripe
from pathlib import Path
import os
from dotenv import load_dotenv
qs = QuickStripe()
df = DateFunction()
hexer = Hexer()
smtp_request = AutoReply()

def o_client(request):
    client_list = Client.objects.exclude(Q(name='Soft Subversion'))
    client_images = Image.objects.exclude(Q(client_id__name="Soft Subversion"))
    project_list = Project.objects.exclude(Q(name="Soft Subversion"))
    project_temp = 0
    image_temp = 0
	# Get query parameters
    project_query = request.GET.get('project')
    client_query = request.GET.get('client')
    order_set = request.GET.get('order')

    # Apply filters
    if project_query:
        project_list = project_list.filter(Q(name__icontains=project_query))
        project_ids = project_list.values_list('id',)
        client_list = client_list.filter(user_id__in=project_ids)

    if client_query:
        client_list = client_list.filter(Q(name__icontains=client_query))
        
	        
    if order_set == 'Oldest':
        client_list = client_list.order_by('id')
    else:
        client_list = client_list.order_by('-id')
   
    clients_info =[]
    for client in client_list:
        client_details = {'client': client.name, 'client_id': client.id, 'client_user': client.user_id}
        for project in project_list:
            if client.user_id == project.user_id:
                project_temp +=1
                for image in client_images:
                    if image.client_id.id == client.id and image.project_id.id == project.id:
                        image_temp +=1
        clients_info.append({'client_details': client_details, 'project_count': project_temp, 'image_count': image_temp})
    print(clients_info)
                	
    return render(request, 'o_panel/client/client.html', {
		'client_info': clients_info,
		'client_images':client_images,
		'project_list': project_list
	})
    
class InviteView(CreateView):
    form_class = InviteForm
    model = Invite
    template_name = 'o_panel/client/client-intake.html'
    
    def form_valid(self, form):
        #try:
        self.object = form.save()
        email = form.cleaned_data.get('email',)
        name = form.cleaned_data.get('email',)
        hex_key = hexer.hex_gen()
        add_feild = self.object
        add_feild.hexkey = hex_key
        add_feild.save()
        response_back = smtp_request.send_invite(email, name, hex_key)
        print(response_back)
    
        if response_back == 'sent':
            dataQ = DataSetUpdate()
            dataQ.json_user_list_check()
            return redirect('o-client')
        else: 
            print('error')
        
        
        #except Exception as e:
            #logging.error("Client Invite Error: %s", str(e))
            #slugified_error_message = slugify(str(e))
            #return redirect('issue-backend', status=508, error_message=slugified_error_message)
        
#---------------------------------------------------------------------------------------------------------#
# Project views
#---------------------------------------------------------------------------------------------------------#

def project_main(request):
    client_list = Client.objects.exclude(Q(name='Soft Subversion'))
    project_images = Image.objects.exclude(Q(client_id__name="Soft Subversion"))
    project_list = Project.objects.exclude(Q(name="Soft Subversion"))
    project_request = ProjectRequest.objects.all()
    project_events = ProjectEvents.objects.all()
    project_temp = 0
    image_temp = 0
    client_name = ''
    
	# Get query parameters
    project_query = request.GET.get('project')
    client_query = request.GET.get('client')
    order_set = request.GET.get('order')
    



    month0, month1, month2, cal, year, todays_date, cal_date = cal_gen()
    # Apply filters
    if project_query:
        project_list = project_list.filter(Q(name__icontains=project_query))


    if client_query:
        client_list = client_list.filter(Q(name__icontains=client_query))
        #client_ids = client_list.values_list('id',)
        #project_list = project_list.filter(user_id__in=client_ids)
	        
    if order_set == 'Oldest':
        project_list = project_list.order_by('id')
    else:
        project_list = project_list.order_by('-id')
   
    project_info =[]
    for project in project_list:

            
        client_name = str(project.user_id.first_name + ' ' + project.user_id.last_name)
        project_details = {
            'project': project.name,
            'project_id': project.id,
            'project_client': client_name,
            'project_status': project.status
                           }
        
        for image in project_images:
            if image.project_id.id == project.id:
                image_temp +=1
        project_info.append({'project_details': project_details, 'image_count': image_temp})
                	
    return render(request, 'o_panel/project/projects.html', {
		'project_info': project_info,
		'project_images':project_images,
		'project_list': project_list,
        'project_request': project_request,
        'project_events': project_events,
        'year': year,
        'month': month1,
        'cal': cal
	})
    

def project_gallery(request, id):
    project = Project.objects.get(id=id)
    image_list = Image.objects.filter(Q(project_id=project))
    image_col1, image_col2, image_col3, new_list, len1, len2 = column_sort(image_list)

    return render(request, 'gallery/project/project-gallery/project-gallery.html', {
        'image_list': image_list,
        'image_col1': image_col1,
        'image_col2': image_col2,
        'image_col3': image_col3,
        'new_list': new_list,
        'len1': len1,
        'len2': len2,
    })

def project_notes(request, id):
    project_terms = ProjectTerms.objects.get(project_id=id)
    project = Project.objects.get(id=id)
    project_request = ProjectRequest.objects.get(id=project_terms.project_request_id.id)
    request_reply = RequestReply.objects.filter(Q(project_request_id=project_request.id))
    
        
    notes = Note.objects.filter(project_id=project_terms.project_id.id)
    new_note = None
    if request.method == 'POST':
        note_form = NotesForm(data=request.POST)
        if note_form.is_valid():
            user_info = request.user
            new_note = note_form.save(commit=False)
            new_note.user_id = user_info
            new_note.project_id = project
            new_note.save()

            return redirect('project-notes', id)

    else:
        note_form = NotesForm()

    return render(request, 'gallery/project/project-notes.html', {
        'request_reply': request_reply,
        'project_terms':project_terms,
        'project_request': project_request,
        'notes': notes,
        'note_form': note_form
    })
    
#---------------------------------------------------------------------------------------------------------#
# Calendar
#---------------------------------------------------------------------------------------------------------#

class ProjectEventsCreate(CreateView):
    model = ProjectEvents
    form_class = ProjectTermsForm
    template_name = 'gallery/project/project-events/new-event.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['project'] = Project.objects.exclude(name='Soft Subversion')
        return context
    def form_invalid(self, form):
        self.objects = form.save(commit=False)
        date = form.cleaned_data.get('date',)
        form.save()
        year, month, day = str(date).split('-')
        return redirect('project-calendar', year=year, month=month)
    

def clandar(request, year, month):
        
    event_list = ProjectEvents.objects.all()
    event_list = ProjectEvents.objects.order_by('date')
    try:
        month_number = int(month)
    except ValueError:
        month = month.title()
        month_number = list(calendar.month_name).index(month)
        month_number = int(month_number) 


    month0, month1, month2, cal, year_new, todays_date, cal_date = cal_gen(month_number, year)
    next_year = year + 1
    last_year = year - 1
    print(year_new)

    return render(request, 'o_panel/project/events/calendar.html', {
        'year': year,
        'month1': month1,
        'month0':month0,
        'month2' :month2,
        'cal': cal,
        'event_list':event_list,
        'last_year': last_year,
        'next_year': next_year,
        'todays_date': todays_date,
        'cal_date': cal_date
    })

#---------------------------------------------------------------------------------------------------------#
# client project request
#---------------------------------------------------------------------------------------------------------#

def project_request(request):
    client_request = ProjectRequest.objects.all()
    request_comments = RequestReply.objects.all()
    request_comments = RequestReply.objects.all()
    project_terms = ProjectTermsForm
    client_request
    return render(request, 'o_panel/project/project_request/project-request.html', {
		'client_request': client_request,
        'request_comments' : request_comments,
        'project_terms': project_terms
  })

def project_request_details(request, id):
    project_request = get_object_or_404(ProjectRequest, id=id)
    print(project_request.id)
    comments = RequestReply.objects.filter(project_request_id=project_request.id)
    new_comments = None
    if request.method == 'POST':
        comment_form = RequestReplyComment(data=request.POST)
        if comment_form.is_valid():
            user_info = request.user
            new_comment = comment_form.save(commit=False)
            new_comment.user_id = user_info
            new_comment.project_request_id = project_request
            new_comment.save()
            comment = comment_form.cleaned_data.get('comment')
            clinet_email = user_info.email
            smtp_request.owner_post_comment(clinet_email, user_info, comment, project_request, id)
            return redirect('comment-success')

    else:
        comment_form = RequestReplyComment()
    
    return render(request, 'o_panel/project/project_request/request-details.html', {
		'projectrequest': project_request,
        'comment_form': comment_form,
        'new_comments' : new_comments,
        'comments': comments, 
  })

def request_approval(request, id):
    try:
        client_request = get_object_or_404(ProjectRequest, id=id)
        user_info = User.objects.get(username=client_request.user_id)
        client_info = Client.objects.get(user_id__username=user_info.username)
        comments = RequestReply.objects.filter(project_request_id=client_request)
        new_template = None

        # Form validation and approval workflow
        if request.method == 'POST':
            terms_form = ProjectTermsForm(data=request.POST)
        
            if terms_form.is_valid():
                
                #----------------------------------------------------------------#
                # structures client and project infromation for addtional methods
                #----------------------------------------------------------------#
                
                # Process cleaned data from terms form
                terms_data = terms_form.cleaned_data
                project_amount = terms_data.get('project_cost')
                deposit_amount = terms_data.get('deposit')
                services = terms_data.get('services')

                # update the project request
                client_request.status = 'Approved'
                client_request.save()
                
                # Extracts users billing information
                full_name, full_address, phone, email_address = qs.stripe_user_extractor(user_info, client_info)
                
                        # check if customer exist in stripe db
                if not client_info.strip_id:
                    stripe_id = qs.stripe_user_creation(
                        client_info, 
                        full_name, 
                        email_address, 
                        full_address, 
                        phone
                    )
                    
                    # Saving new strip customer id
                    client_info.strip_id = stripe_id
                    client_info.save()
                else:
                    stripe_id = client_info.strip_id

                #----------------------------------------------------------------#
                # creates the corresponding prject, billing and project-terms
                #----------------------------------------------------------------#
                
                # creates project
                new_project_model = Project.objects.create(
                    name=client_request.name,
                    user_id=user_info,
                    client_id=client_info
                )
                
                # creates the billing corresponding stripe invoice for the project
                request_date_distance = df.date_distance(client_request.date)
                project_date_distance = request_date_distance + 30
                strip_project_invoice = qs.create_stripe_invoice(stripe_id, project_date_distance, services)

                # creates new billing account for client 
                new_billing_model = Invoice.objects.create(
                    project_id=new_project_model,
                    invoice_id=strip_project_invoice.id,
                    status = strip_project_invoice.status,
                    details=services,
                    due_date = df.number_to_days(project_date_distance),
                    payment_type='Project Invoice'
                )
                
                # creates new Project Terms  
                new_template = terms_form.save(commit=False)
                
                new_template.user_id = user_info
                new_template.project_request_id = client_request
                new_template.scope = client_request.scope
                new_template.project_docs = f"{user_info}/{client_request.name}"
                new_template.project_id = new_project_model
                
                new_template.save()
                #----------------------------------------------------------------#
                # checks for deposit and project cost and process if they exist
                #----------------------------------------------------------------#
                converted_to_cents = lambda dollar_amount: int(
                    str(
                        '{:.2f}'.format(
                            float(dollar_amount))).replace('.','')
                )
                if deposit_amount > 0:
                    deposit_date = df.deposit_distance(client_request.date)
                    deposit_details = f'Deposit for photography project:{new_project_model.name}'
                    deposit = converted_to_cents(deposit_amount)
                    deposit_invoice = qs.create_stripe_invoice(stripe_id, deposit_date, deposit_details)

                    
                    deposit_lineitem = qs.create_stripe_line_item(deposit, 'Deposit Cost', deposit_invoice, stripe_id)
                    payment_link, deposit_invoice_update = qs.send_stripe_invoice(deposit_invoice.id)
                    deposit_billing = Invoice.objects.create(
                        project_id=new_project_model,
                        invoice_id=deposit_invoice.id,
                        details=deposit_details,
                        billed=deposit_amount,
                        status=deposit_invoice_update.status,
                        due_date = df.number_to_days(deposit_date),
                        payment_link=payment_link,
                        payment_type='Deposit'
                    )
                    
                    LineItem.objects.create(
                        billing_id=deposit_billing,
                        amount=deposit_amount,
                        receipt='Deposit Cost',
                        time_stamp=df.date_now(),
                        item_id=deposit_lineitem.id,
                    )
                    
                    ProjectEvents.objects.create(
                        title='Deposit Reminder',
                        project_id=new_project_model,
                        billing_id=new_billing_model,
                        date=new_billing_model.due_date,
                        start=df.payment_time(),
                        end=df.payment_time(),
                        event_type='Payment Reminder',
                        details=f'Event for deposit reminder for project{new_project_model}'
                    )
    
                    qs.send_invoice_email(user_info, new_project_model, deposit_billing)

                if project_amount > 0:
                    project_cost = converted_to_cents(project_amount)
                    project_lineitem = qs.create_stripe_line_item(project_cost, 'Project Cost', strip_project_invoice, stripe_id)
                    LineItem.objects.create(
                        billing_id=new_billing_model,
                        amount=project_amount,
                        receipt='Project Cost',
                        time_stamp=df.date_now(),
                        item_id=project_lineitem.id,
                    )
                    
                    new_billing_model.billed = project_amount
                    new_billing_model.save()
                    
            return redirect('project-details', new_project_model.id)

        else:
            terms_form = ProjectTermsForm()
            
        return render(request, 'o_panel/project/project_request/request-approval.html', {
            'client_request': client_request,
            'user_info': user_info,
            'comments': comments,
            'client_info': client_info,
            'terms_form': terms_form,
            'new_template': new_template
        })
        
    except Exception as e:
        logging.error("Stripe customer create method failed: %s", str(e))
        return redirect('issue-backend')
    
    
#----------------------------------------------------------------#
# client panel views 
#----------------------------------------------------------------#

def c_panel(request, id):
    users_id = id
    client = Client.objects.get(user_id=users_id)
    client_id = client.id
    client_images = Image.objects.filter(client_id=client_id)
    project_list = Project.objects.filter(client_id=client_id)
    project_request_info = ProjectRequest.objects.filter(client_id=client_id)
    request_comments = RequestReply.objects.filter(user_id__id=users_id)
                	
    return render(request, 'c_panel/project/binder.html', {
		'client_info': client,
		'client_images':client_images,
		'project_list': project_list,
        'project_request': project_request_info,
        'comments': request_comments
	})
    
class ClienRequestCreate(CreateView):
    form_class = ProjectRequestForm
    model = ProjectRequest
    
    template_name = 'c_panel/project/request/new-request.html'
    def form_valid(self, form):

        
        user_info = self.request.user
        user_id = user_info.id
        client = user_info.username
        user_info.user_id = user_id
        
        project_name = form.cleaned_data.get('name')
        date_selected = form.cleaned_data.get('date')
        scope = form.cleaned_data.get('scope')
        details = form.cleaned_data.get('details')
        location_type = form.cleaned_data.get('location')


        
        project_request = form.save(commit=False)
        
        id_str = str(user_id)
        project_name_str = str(project_name)
        clean_name = project_name_str.replace(' ', '-')
        randnum = hexer.hex_gen_small()
        pj_id = str(randnum)

        slug_str = str(id_str + '-' + pj_id + '-' + 'prj')
        
        project_request.user_id_id = user_id 
        project_request.slug = slug_str
        project_request.save()
        
        smtp_request.project_request_notice(project_name, date_selected, scope, details, location_type, user_id, client)
        return redirect('request-status', project_request.id)
    
def request_status(request, id):
    project_request = get_object_or_404(ProjectRequest, id=id)
    print(project_request.id)
    comments = RequestReply.objects.filter(project_request_id=project_request.id)
    new_comments = None
    if request.method == 'POST':
        comment_form = RequestReplyComment(data=request.POST)
        if comment_form.is_valid():
            user_info = request.user
            new_comment = comment_form.save(commit=False)
            new_comment.user_id = user_info
            new_comment.project_request_id = project_request
            new_comment.save()
            comment = comment_form.cleaned_data.get('comment')
            return redirect('client-comment-success')

    else:
        comment_form = RequestReplyComment()
    
    return render(request, 'c_panel/project/request/request-status.html', {
		'projectrequest': project_request,
        'comment_form': comment_form,
        'new_comments' : new_comments,
        'comments': comments, 
  })
    
    