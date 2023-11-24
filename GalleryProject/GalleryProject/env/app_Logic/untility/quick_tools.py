from datetime import datetime, timedelta
import stripe
from GalleryProject.env.app_Logic.smtp.MailerDJ import AutoReply
from GalleryProject.env.cloudflare_API.CFAPI import APICall
import secrets
from pathlib import Path
import os
from dotenv import load_dotenv
from django.shortcuts import redirect
import time

current_dir = Path(__file__).resolve().parent
ven = current_dir / "../.env"
load_dotenv(ven)
stripe.api_key = os.getenv("STRIPE_KEY")
cf_images = APICall()

class DocumentFunctions:
	def __init__(self):
		self.model_path = 'pdfs/Model-Photo-questionnaire.pdf'
		self.family_path = 'pdfs/Family-Photo-questionnaire.pdf'
		self.wedding_path = 'pdfs/Wedding-Photo-questionnaire.pdf'
	
	def pdf_path_finder(self, scope):
		#sets up PDf questionair path 
		if scope == 'model':
			pdf_path = self.model_path

		elif scope == 'family':
			pdf_path = self.family_path
			
		elif scope == 'wedding':
			pdf_path = self.wedding_path
		else:	
			pdf_path = self.family_path

		return pdf_path


# -------------------------------------------------------------------------------------------------------------#
# Date and time configeration
# -------------------------------------------------------------------------------------------------------------#


class DateFunction:
	def number_to_days(self, numbs):
		date_and_time = datetime.now()
		dates = date_and_time.date()
		new_date = dates + timedelta(days=numbs)
		return new_date

	def date_now(self):
		date_and_time = datetime.now()
		dates = date_and_time.date()
		return dates

	def year_now(self):
		year = datetime.now().year
		return year

	def date_distance(self, desired_date):
		due_in = ''
		desired_date_str = str(desired_date)
		date_sets = ["%d-%m-%Y", "%Y-%m-%d", "%m-%d-%Y", "%d-%m-%y", "%y-%m-%d", "%m-%d-%y", "%M-%d-%y", "%M-%d-%y"]
		for date_format in date_sets:
			try:
				requested_date = datetime.strptime(desired_date_str, date_format).date()
	
			except ValueError as e:
				pass
				
		date_and_time = datetime.now()
		dates = date_and_time.date()
		
		due_in = (requested_date - dates).days
		return due_in


	def deposit_distance(self, desired_date):
		desired_date_str = str(desired_date)

		
		requested_date = datetime.strptime(desired_date_str, "%Y-%m-%d").date()
		date_and_time = datetime.now()
		dates = date_and_time.date()
		
		if (requested_date - dates).days <= 30:
			due_in = 5
			
		else:
			due_in = 30

			
		return due_in 

	def payment_time(self):
		return datetime.strptime("5:00 pm", "%I:%M %p").time()

	def DMY_date_format(self, date):
		formated_date = datetime.strftime(date, '%d-%b-%Y')
		return formated_date

	def DmY_date_format(self, date):
		formated_date = datetime.strftime(date, '%d-%m-%Y')
		return formated_date
  
#-------------------------------------------------------------------------------------------------------#
# hex_gen
#-------------------------------------------------------------------------------------------------------#
class Hexer:
	def hex_gen(self):
		random_hex = secrets.token_hex(16)
		return str(random_hex)

	def hex_gen_small(self):
		random_hex = secrets.token_hex(4)
		return str(random_hex)


#-------------------------------------------------------------------------------------------------------#
# smtp global
#-------------------------------------------------------------------------------------------------------#

smtp_request = AutoReply()

#-------------------------------------------------------------------------------------------------------#
# ownder client views 
#-------------------------------------------------------------------------------------------------------#


class QuickStripe:

	def slug_string_construction(self, slug):
			# Slug forr the project is created here
		if len(str(slug)) > 16:
			model_object_slug = 'terms' + str(slug[0:17]) + Hexer.hex_gen_small()
		else:
			model_object_slug = 'terms' + str(slug) + Hexer.hex_gen_small()
		return model_object_slug

		
	def stripe_user_creation(self, client_info, full_name, email_address, full_address, phone):

		strip_customer = stripe.Customer.create(
			name=full_name,
			email=email_address,
			address=full_address,
			phone=phone
		)

		stripe_id = strip_customer.id

		return stripe_id
			
	def stripe_user_extractor(self, user_info, client_info):

		# Extract and format client info forr Stripe request
		firstname = user_info.first_name
		lastname = user_info.last_name
		address1 = client_info.address_1
		address2 = client_info.address_2
		phone = client_info.phone
		city = client_info.city
		state = client_info.state
		zipcode = client_info.zip_code

		full_name = f"{firstname} {lastname}"

		full_address = {'line1':address1, 'line2':address2, 'city':city, 'state': state, 'postal_code':zipcode, 'country':'US'  }
		email_address = user_info.email

		return full_name, full_address, phone, email_address
			
	def create_stripe_invoice(self, stripe_id, due_date, services):
		return stripe.Invoice.create(
			customer=stripe_id,
			collection_method='send_invoice',
			days_until_due=due_date,
			description=services,
		)

	def create_stripe_line_item(self, amount_charged, receipt, stripe_invoice, stripe_id):
		return stripe.InvoiceItem.create(
			amount=amount_charged,
			currency='usd', 
			description= receipt,
			discountable= False,
			invoice=stripe_invoice.id,
			customer=stripe_id
		)
	def stripe_cash_payment(self, stripe_invoice_id):
		return stripe.Invoice.pay(
			stripe_invoice_id,
			paid_out_of_band=True
		)
  
	def stripe_update_invoice(self, stripe_invoice, due_date,services ):
		return stripe.Invoice.modify(
			stripe_invoice,
   			days_until_due=due_date,
			description=services
		)
  
	def delete_stripe_draft(self, stripe_invoice_id):
		return stripe.Invoice.delete(
			stripe_invoice_id
		)
  
	def void_stripe_invoice(self, stripe_invoice_id):
		return stripe.Invoice.void_invoice(
			stripe_invoice_id
		)
  
	def send_stripe_invoice (self, invoice_id):
		# send the invoice and pulls the payment link and the new invoice data 
		invoice_out = stripe.Invoice.send_invoice(invoice=invoice_id)
		payment_link = invoice_out.hosted_invoice_url
		invoice_update = stripe.Invoice.retrieve(id=invoice_id)
		return payment_link, invoice_update

	def get_strripe_invoice_link(self, stripe_id):
		strip_object = stripe.Invoice.retrieve(id=stripe_id)
		return strip_object.hosted_invoice_url

	def send_invoice_email(self, user_info, project, invoice, pdf_path):
		project_link = f"https://SoftSubversion.com/c-panel/binder/project/{project.slug}/"
		invoice_link = f"https://SoftSubversion.com/c-panel/binder/invoice/{invoice.id}/"
		smtp_request.send_new_project_and_invoice(
	  		user_info,
   			project,
			invoice,
			project_link,
			invoice_link,
   			pdf_path,
		)   
  
  
	def send_project_only_email(self, user_info, project, pdf_path):
		project_link = f"https://SoftSubversion.com/c-panel/binder/project/{project.slug}/"
		smtp_request.send_new_project_no_invoice(
		user_info,
  		project,
		project_link,
		pdf_path
		) 
  
	def new_invoice(self, user_info, project, pdf_path):
		smtp_request.new_invoice_notice(
		user_info,
  		project,
		pdf_path
		) 
  
	def resend_invoice(self, user_info, project, payment_link, invoice, pdf_path):
		smtp_request.resend_invoice_notice(
		user_info,
  		project,
		invoice,
		payment_link,
	 	pdf_path
		) 
  
#-------------------------------------------------------------------------------------------------------#
# view functions extened 
#-------------------------------------------------------------------------------------------------------#

class ViewExtendedFunctions:
	def __init__(self):
		self.qs = QuickStripe()
		self.df = DateFunction()
  
  
	def new_invoice(self, invoice_model, project, invoice_details, invoice_total, line_items_cost, line_items_receipt, line_item_model, event_model):
		#try: 		
		# sets vars for frrom data
		converted_to_cents = lambda dollar_amount: int(str('{:.2f}'.format(float(dollar_amount))).replace('.',''))
		stripe_date = self.df.date_distance(invoice_details.get('due_date'))
		set_payment_type = invoice_details.get('payment_type')
		set_details = f"{set_payment_type} for photography project:{project.name}"
		
		# Get strip ID from client            
		stripe_id = project.client_id.strip_id
		
		# strip invoice and project billing 
		set_invoice = self.qs.create_stripe_invoice(stripe_id, stripe_date, set_details)
		new_billing = invoice_model.objects.create(
				project_id=project,
				invoice_id=set_invoice.id,
				billed = invoice_total,
				details = set_details,
				due_date = self.df.number_to_days(stripe_date),
				payment_type=set_payment_type
		)

		# checks for and creates line item and billing payments 
		if line_items_cost:
			for cost, receipt in zip(line_items_cost.values(), line_items_receipt.values()):
				
				stripe_cost = converted_to_cents(cost)
				set_lineitem = self.qs.create_stripe_line_item(stripe_cost, receipt, set_invoice, stripe_id)
				line_item_model.objects.create(
					billing_id=new_billing,
					amount=cost,
					receipt=receipt,
					time_stamp=self.df.date_now(),
					item_id=set_lineitem.id,
				)

				time.sleep(5)
		
		if invoice_details.get('open'):
			payment_link, invoice_update = self.qs.send_stripe_invoice(set_invoice.id)
			new_billing.payment_link = payment_link
			new_billing.status = invoice_update.status
			new_billing.save()
			event_model.objects.create(
				title='Deposit Reminder',
				project_id=project,
				billing_id=new_billing,
				date=new_billing.due_date,
				start=self.df.payment_time(),
				end=self.df.payment_time(),
				event_type='Payment Reminder',
				details=f'Event for deposit reminder for project{project}'
			)

		if invoice_details.get('paidCash'):
			invoice_update = self.qs.stripe_cash_payment(set_invoice.id)
			new_billing.status = invoice_update.status
			new_billing.paid = invoice_total
			new_billing.fufiled = True
			new_billing.save()

		return 'success'	

		#except Exception as e:
			#return f'Invoice Creation Error:{e}'


	def open_draft_invoice(self, client, project, invoice_id, billing_list, pdf_path):

		#try:
		invoice = billing_list.get(id=invoice_id)
		
		if invoice.status == "draft":
			payment_link, invoice_update = self.qs.send_stripe_invoice(invoice.invoice_id)
			invoice.payment_link = payment_link
			invoice.status = invoice_update.status
			invoice.save()
		if invoice.status =='open':
			payment_link = self.qs.get_strripe_invoice_link(invoice.invoice_id)
			self.qs.resend_invoice(client, project, payment_link, invoice, pdf_path)
		return 'success'	

		#except Exception as e:
			#return f'Invoice Operation Error:{e}'


	def delete_or_void_invoice(self, invoice):
	 
		if invoice.status !='open' or invoice.status == "draft":

			return 'Invoice is already voided or deleted'
		else: 
			try:
				if invoice.status == "draft":
					self.qs.delete_stripe_draft(invoice.invoice_id)
					invoice.delete()

				if invoice.status =='open':
					void_invoice = self.qs.void_stripe_invoice(invoice.invoice_id)
					invoice.status = void_invoice.status
					invoice.save()
				return 'success'

			except Exception as e:
				return f'Invoice Operation Error:{e}'


	def invoice_paid_in_cash(self, invoice):
		try:
			invoice_update = self.qs.stripe_cash_payment(invoice.invoice_id)
			invoice.fufiled = True
			invoice.paid = invoice.billed
			invoice.status = invoice_update.status
			invoice.save()
			
			return 'success'

		except Exception as e:
			return f'Invoice Operation Error:{e}'

	
	def delete_project(self, project, project_terms,images, notes, project_events, billing_list ):
		try:
			for pic in images:
				cf_images.delete_image(pic.cloudflare_id)
				pic.delete()
			
			for note in notes:
				note.delete()
			
			for events in project_events:
				events.delete()
				
			for bill in billing_list:
				if bill.status == 'draft':
					self.qs.delete_stripe_draft(bill.invoice_id)
					bill.delete()
		
				elif bill.status == 'open':
					self.qs.void_stripe_invoice(bill.invoice_id)
		
				elif bill.status == 'paid' or bill.status == 'void' or bill.status == 'uncollectible':
					pass
				
			project_terms.delete()    
			project.delete()
			return 'success'

		except Exception as e:
			return f'Invoice Operation Error:{e}'

