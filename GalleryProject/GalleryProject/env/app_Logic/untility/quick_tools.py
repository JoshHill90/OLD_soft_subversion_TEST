from datetime import datetime, timedelta
import stripe
from GalleryProject.env.app_Logic.smtp.MailerDJ import AutoReply
import secrets

from pathlib import Path
import os
from dotenv import load_dotenv
from django.shortcuts import render, redirect, get_object_or_404
from log_app.logging_config import logging

current_dir = Path(__file__).resolve().parent
ven = current_dir / "../.env"
load_dotenv(ven)
stripe.api_key = os.getenv("STRIPE_KEY")
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

        
	def send_invoice_email(self, user_info, project, invoice):
		project_link = f"https://SoftSubversion.com/client-portal/project-binder/{project.id}/details"
		invoice_link = f"https://SoftSubversion.com/client-portal/billing/{invoice.id}/"
		smtp_request.new_project_and_invoice(user_info.email,
			user_info.first_name,
			invoice.payment_link,
			project_link,
			invoice_link
		)   
  
	def resend_invoice(self, user_info, project, invoice):
		project_link = f"https://SoftSubversion.com/client-portal/project-binder/{project.id}/details"
		invoice_link = f"https://SoftSubversion.com/client-portal/billing/{invoice.id}/"
		smtp_request.new_project_and_invoice(user_info.email,
			user_info.first_name,
			invoice.payment_link,
			project_link,
			invoice_link
		) 