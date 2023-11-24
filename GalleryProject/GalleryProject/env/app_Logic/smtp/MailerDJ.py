import ssl
import smtplib
from ..text_py.text_for_emails import *
from email.message import EmailMessage
from email.utils import formataddr
from pathlib import Path
import os
from dotenv import load_dotenv
from functools import reduce
import datetime
current_dir = Path(__file__).resolve().parent
ven = current_dir / "../.." / ".env"
load_dotenv(ven)




#-------------------------------------------------------------------------------------------------------#
# Secret Values
#-------------------------------------------------------------------------------------------------------#


class AutoReply:

    email_host = os.getenv("EMAIL_HOSTING")
    send_from = os.getenv("EMAIL_USER")
    email_password = os.getenv("EMAIL_PASSWORD")
    email_port = os.getenv("EMAIL_PORT")
    email_backend = os.getenv("EMAIL_BACKEND_SMTP")
    alart_email = os.getenv("EMAIL_USER")
    receive_email = os.getenv("RECEIVE_EMAILS")
    #------------------------#
    # Contact form auto reply
    #------------------------#

    def request_project_comment(self, user, comment, project_name, slug):
        print('preparing message')

        contact_subject = "New Comment in Project Request"

        if user.id == 1:
            links = f'https://softsubversion.com/o-panel/binder/project/requests/{slug}'
        else:
            links = f'https://softsubversion.com/c-panel/binder/requests/{slug}'

        text_swap = {
            '[USER_NAME]': user.first_name, 
            '[PROJECT_NAME]': project_name, 
            '[COMMENT]': comment, 
            '[LINK]': links
        }
        
        print(text_swap)
        string = request_post_comment
        result_string = reduce(lambda old_string, key_var: old_string.replace(key_var, text_swap[key_var]), text_swap, string)

        contact_body = result_string
        mailer = EmailMessage()
        print(result_string)
        mailer['From'] = formataddr(("Soft Subversion", f"{self.send_from}"))
        mailer['To'] = user.email
        mailer['Subject'] = contact_subject
        mailer.set_content(contact_body)

        with smtplib.SMTP(self.email_host, self.email_port) as server:
            try:
                server.starttls()
                server.login(self.send_from, self.email_password)
                server.sendmail(self.send_from, user.email, mailer.as_string())
                server.close()
                print('email sent')
            except Exception as e:
                print(f"An error occurred while sending the email: {e}")
    
    #------------------------#
    # Contact form auto reply
    #------------------------#

    def contact_request(self, user_email, user_name, user_subject):
        print('preparing message')

        contact_subject = "Thank You for Contacting Soft Subversion!"

        text_swap = {
            '[USER_NAME]' : user_name,
            '[USER_SUBJECT]' : user_subject
        }
        string = contact_request_body
        result_string = reduce(lambda old_string, key_var: old_string.replace(key_var, text_swap[key_var]), text_swap, string)
        contact_body = result_string


        mailer = EmailMessage()

        mailer['From'] = formataddr(("Soft Subversion", f"{self.send_from}"))
        mailer['To'] = user_email
        mailer['Subject'] = contact_subject
        mailer.set_content(contact_body)

        with smtplib.SMTP(self.email_host, self.email_port) as server:
            try:
                server.starttls()
                server.login(self.send_from, self.email_password)
                server.sendmail(self.send_from, user_email, mailer.as_string())
                server.close()
                print('email sent')
            except Exception as e:
                print(f"An error occurred while sending the email: {e}")


    #------------------------#
    # Email Alart
    #------------------------#

    def contact_alart(self, email, user_name, user_subject, body):

        contact_subject = "Contact Form Alart"

        text_swap = {
            '[USER_NAME]' : user_name,
            '[SUBJECT]' : user_subject, 
            '[BODY]': body, 
            '[USER_EMAIL] ': email
        }
        string = contact_alart_body
        result_string = reduce(lambda old_string, key_var: old_string.replace(key_var, text_swap[key_var]), text_swap, string)
        contact_body = result_string


        mailer = EmailMessage()

        mailer['From'] = formataddr(("Contact Form", f"{self.alart_email}"))
        mailer['To'] = self.receive_email
        mailer['Subject'] = contact_subject
        mailer.set_content(contact_body)

        with smtplib.SMTP(self.email_host, self.email_port) as server:
            try:
                server.starttls()
                server.login(self.send_from, self.email_password)
                server.sendmail(self.send_from, self.receive_email, mailer.as_string())
                server.close()
                print('alart sent')
            except Exception as e:
                print(f"An error occurred while sending the email: {e}")
    
    #------------------------#
    # Client invite
    #------------------------#

    def send_invite(self, client_email, client_name, hexkey):
        print(self.email_port, ' port')
        contact_subject = "Your Exclusive Registration Key for Soft Subversion's Online Studio"

        text_swap = {'[CLIENT_NAME]': client_name,
                     '[REG_URL]': 'https://softsubversion.com/register',
                     '[REG_KEY]': hexkey
                     }
        
        string = send_invite_text
        result_string = reduce(lambda old_string, key_var: old_string.replace(key_var, text_swap[key_var]), text_swap, string)
        contact_body = result_string

        mailer = EmailMessage()

        mailer['From'] = formataddr(("Soft Subversion", f"{self.email_host}"))
        mailer['To'] = client_email
        mailer['Subject'] = contact_subject
        mailer.set_content(contact_body)

        with smtplib.SMTP(self.email_host, self.email_port) as server:
            try:
                server.starttls()
                server.login(self.send_from, self.email_password)
                server.sendmail(self.send_from, client_email, mailer.as_string())
                server.close()
                return 'sent'
            except Exception as e:
                print(f"An error occurred while sending the email: {e}")
                
    #------------------------#
    # Project Request
    #------------------------#

    def project_request_notice(self, project_name, date_selected, scope, details, location, user_id, client_name):
        user_id = str(user_id) + '-1'
        contact_subject = "Project Request"

        text_swap = {'[CLIENT_NAME]': client_name,
                     '[USER_ID]': user_id,
                     '[PROJECT_NAME]': project_name,
                     '[SCOPE]': scope,
                     '[DATE_SELECTED]': date_selected,
                     '[LOCATION]': location, 
                     '[DETAILS]': details }
        
        string = project_request_notice_body
        result_string = reduce(lambda old_string, key_var: old_string.replace(key_var, text_swap[key_var]), text_swap, string)
        contact_body = result_string

        mailer = EmailMessage()

        mailer['From'] = formataddr(("Soft Subversion", f"{self.alart_email}"))
        mailer['To'] = self.receive_email
        mailer['Subject'] = contact_subject
        mailer.set_content(contact_body)

        with smtplib.SMTP(self.email_host, self.email_port) as server:
            try:
                server.starttls()
                server.login(self.send_from, self.email_password)
                server.sendmail(self.send_from, self.receive_email, mailer.as_string())
                server.close()
                print('alart sent')
            except Exception as e:
                print(f"An error occurred while sending the email: {e}")
                
    #------------------------#
    # project/invoice creation
    #------------------------#

    def send_new_project_and_invoice(self, client_info, project, invoice, project_link, invoice_link, pdf_path):

        contact_subject = "New Project in your Project Binder"
        billing_amount_formated = '{:.2f}'.format(invoice.billed)
        billed_amount_str = str(billing_amount_formated)
        date_value = invoice.due_date.strftime('%b-%d-%Y')

        
        text_swap = {
            '[CLIENT_NAME]': client_info.first_name,
            '[PAYMENT_LINK]': invoice.payment_link,
            '[PROJECT_LINK]': project_link,
            '[INVOICE_LINK]': invoice_link,
            '[PROJECT_NAME]': project.name,
            '[INVOICE_NUMBER]': invoice.invoice_id,
            '[DUE_DATE]': str(date_value),
            '[PAYMENT_DUE]': billed_amount_str,
            '[PAYMENT_TYPE]': invoice.payment_type
            }
        
        string = new_project_and_invoice
        result_string = reduce(lambda old_string, key_var: old_string.replace(key_var, text_swap[key_var]), text_swap, string)
        contact_body = result_string

        mailer = EmailMessage()

        mailer['From'] = formataddr(("Soft Subversion", f"{self.email_host}"))
        mailer['To'] = client_info.email
        mailer['Subject'] = contact_subject
        mailer.set_content(contact_body)
        full_path = 'static/documents/'+ pdf_path
        with open(full_path, 'rb') as attachment:
            mailer.add_attachment(attachment.read(), 
                                  maintype='application', 
                                  subtype='octet-stream', 
                                  filename='Soft Subversion Questionnaire.pdf'
            )

        with smtplib.SMTP(self.email_host, self.email_port) as server:
            try:
                server.starttls()
                server.login(self.send_from, self.email_password)
                server.sendmail(self.send_from, client_info.email, mailer.as_string())
                server.close()
                return 'sent'
            except Exception as e:
                print(f"An error occurred while sending the email: {e}")
                
                
    #------------------------#
    # project without invoice
    #------------------------#

    def send_new_project_no_invoice(self, client_info, project, project_link, pdf_path):

        contact_subject = "New Project in your Project Binder"

        text_swap = {
            '[CLIENT_NAME]': client_info.first_name,
            '[PROJECT_LINK]': project_link,
            '[PROJECT_NAME]': project.name,
            }
        
        string = new_project_no_invoice
        result_string = reduce(lambda old_string, key_var: old_string.replace(key_var, text_swap[key_var]), text_swap, string)
        contact_body = result_string

        mailer = EmailMessage()

        mailer['From'] = formataddr(("Soft Subversion", f"{self.email_host}"))
        mailer['To'] = client_info.email
        mailer['Subject'] = contact_subject
        mailer.set_content(contact_body)
        full_path = 'static/documents/'+ pdf_path
        with open(full_path, 'rb') as attachment:
            mailer.add_attachment(attachment.read(), 
                                  maintype='application', 
                                  subtype='octet-stream', 
                                  filename='Soft Subversion Questionnaire.pdf'
            )

        with smtplib.SMTP(self.email_host, self.email_port) as server:
            try:
                server.starttls()
                server.login(self.send_from, self.email_password)
                server.sendmail(self.send_from, client_info.email, mailer.as_string())
                server.close()
                return 'sent'
            except Exception as e:
                print(f"An error occurred while sending the email: {e}")
                
                
    def new_invoice_notice(self, client_info, project, invoice, invoice_link, pdf_path):
        
        contact_subject = f"New Invoice: {project.name} Invoice {invoice.invoice_id}"
        billing_amount_formated = '{:.2f}'.format(invoice.billed)
        billed_amount_str = str(billing_amount_formated)
        date_value = invoice.due_date.strftime('%b-%d-%Y')

        
        text_swap = {
            '[CLIENT_NAME]': client_info.first_name,
            '[PAYMENT_LINK]': invoice.payment_link,
            '[INVOICE_LINK]': invoice_link,
            '[PROJECT_NAME]': project.name,
            '[INVOICE_NUMBER]': invoice.invoice_id,
            '[DUE_DATE]': str(date_value),
            '[PAYMENT_DUE]': billed_amount_str,
            '[PAYMENT_TYPE]': invoice.payment_type
            }
        
        string = new_project_no_invoice
        result_string = reduce(lambda old_string, key_var: old_string.replace(key_var, text_swap[key_var]), text_swap, string)
        contact_body = result_string

        mailer = EmailMessage()

        mailer['From'] = formataddr(("Soft Subversion", f"{self.email_host}"))
        mailer['To'] = client_info.email
        mailer['Subject'] = contact_subject
        mailer.set_content(contact_body)
        full_path = 'static/documents/'+ pdf_path
        with open(full_path, 'rb') as attachment:
            mailer.add_attachment(attachment.read(), 
                                  maintype='application', 
                                  subtype='octet-stream', 
                                  filename='Soft Subversion Questionnaire.pdf'
            )

        with smtplib.SMTP(self.email_host, self.email_port) as server:
            try:
                server.starttls()
                server.login(self.send_from, self.email_password)
                server.sendmail(self.send_from, client_info.email, mailer.as_string())
                server.close()
                return 'sent'
            except Exception as e:
                print(f"An error occurred while sending the email: {e}")
                
    def resend_invoice_notice(self, client_info, project, invoice, invoice_link, pdf_path):
        
        contact_subject = f"Reminder: {project.name} Invoice {invoice.invoice_id} Due Soon"
        billing_amount_formated = '{:.2f}'.format(invoice.billed)
        billed_amount_str = str(billing_amount_formated)
        date_value = invoice.due_date.strftime('%b-%d-%Y')

        
        text_swap = {
            '[CLIENT_NAME]': client_info.user_id.first_name,
            '[PAYMENT_LINK]': invoice.payment_link,
            '[INVOICE_LINK]': invoice_link,
            '[PROJECT_NAME]': project.name,
            '[INVOICE_NUMBER]': invoice.invoice_id,
            '[DUE_DATE]': str(date_value),
            '[PAYMENT_DUE]': billed_amount_str,
            '[PAYMENT_TYPE]': invoice.payment_type
            }
        
        string = resend_invoice
        result_string = reduce(lambda old_string, key_var: old_string.replace(key_var, text_swap[key_var]), text_swap, string)
        contact_body = result_string

        mailer = EmailMessage()

        mailer['From'] = formataddr(("Soft Subversion", f"{self.email_host}"))
        mailer['To'] = client_info.email
        mailer['Subject'] = contact_subject
        mailer.set_content(contact_body)
        full_path = 'static/documents/'+ pdf_path
        with open(full_path, 'rb') as attachment:
            mailer.add_attachment(attachment.read(), 
                                  maintype='application', 
                                  subtype='octet-stream', 
                                  filename='Soft Subversion Questionnaire.pdf'
            )

        with smtplib.SMTP(self.email_host, self.email_port) as server:
            try:
                server.starttls()
                server.login(self.send_from, self.email_password)
                server.sendmail(self.send_from, client_info.email, mailer.as_string())
                server.close()
                return 'sent'
            except Exception as e:
                print(f"An error occurred while sending the email: {e}")
                
                
#### Test 
"""test_send = os.getenv("TEST_SEND")

subject_test = "TEST"

body_test ="body"

SMTP = AutoReply()

SMTP.contact_request(test_send, 'john')
print('smtp request')
SMTP.contact_alart(test_send, 'john', subject_test, body_test)"""

