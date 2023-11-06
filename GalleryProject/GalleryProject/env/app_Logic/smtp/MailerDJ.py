import ssl
import smtplib
from..text_py.text_for_emails import *
from email.message import EmailMessage
from email.utils import formataddr
from pathlib import Path
import os
from dotenv import load_dotenv
from functools import reduce

current_dir = Path(__file__).resolve().parent
ven = current_dir / "../.env"
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
    owners_email = os.getenv("REMAIL_CONTACT")
    
    #------------------------#
    # Contact form auto reply
    #------------------------#

    def owner_post_comment(self, user_email, user_name, comment, project_name, slug):
        print('preparing message')

        contact_subject = "Thank You for Contacting Soft Subversion!"

        user_nameS = str(user_name)
        project_nameS = str(project_name)
        commentS = str(comment)
        linkS = str(slug)
        
        

        text_swap = {'user_name': user_nameS, 'project_name': project_nameS, 'comment': commentS, 'link': linkS}
        print(text_swap)
        string = owner_post_comment_body
        result_string = reduce(lambda old_string, key_var: old_string.replace(key_var, text_swap[key_var]), text_swap, string)

        contact_body = result_string
        mailer = EmailMessage()
        print(result_string)
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
    # Contact form auto reply
    #------------------------#

    def contact_request(self, user_email, user_name, user_subject):
        print('preparing message')

        contact_subject = "Thank You for Contacting Soft Subversion!"

        text_swap = {'user_name' : user_name, 'user_subject' : user_subject}
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

        text_swap = {'user_name' : user_name, 'user_subject' : user_subject, 'body': body, 'user_email': email}
        string = contact_request_body
        result_string = reduce(lambda old_string, key_var: old_string.replace(key_var, text_swap[key_var]), text_swap, string)
        contact_body = result_string


        mailer = EmailMessage()

        mailer['From'] = formataddr(("Contact Form", f"{self.send_from}"))
        mailer['To'] = self.owners_email
        mailer['Subject'] = contact_subject
        mailer.set_content(contact_body)

        with smtplib.SMTP(self.email_host, self.email_port) as server:
            try:
                server.starttls()
                server.login(self.send_from, self.email_password)
                server.sendmail(self.send_from, self.owners_email, mailer.as_string())
                server.close()
                print('alart sent')
            except Exception as e:
                print(f"An error occurred while sending the email: {e}")
    
    #------------------------#
    # Client invite
    #------------------------#

    def send_invite(self, client_email, client_name, hexkey):

        contact_subject = "Your Exclusive Registration Key for Soft Subversion's Online Studio"

        text_swap = {'[client_name]': client_name,
                     '[REG_URL]': 'softsubversion.com/register',
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

        text_swap = {'client_name': client_name,
                     'user_id': user_id,
                     'project_name': project_name,
                     'scope': scope,
                     'date_selected': date_selected,
                     'location': location, 
                     'details': details }
        
        string = project_request_notice_body
        result_string = reduce(lambda old_string, key_var: old_string.replace(key_var, text_swap[key_var]), text_swap, string)
        contact_body = result_string

        mailer = EmailMessage()

        mailer['From'] = formataddr(("Soft Subversion", f"{self.send_from}"))
        mailer['To'] = self.owners_email
        mailer['Subject'] = contact_subject
        mailer.set_content(contact_body)

        with smtplib.SMTP(self.email_host, self.email_port) as server:
            try:
                server.starttls()
                server.login(self.send_from, self.email_password)
                server.sendmail(self.send_from, self.owners_email, mailer.as_string())
                server.close()
                print('alart sent')
            except Exception as e:
                print(f"An error occurred while sending the email: {e}")
                
    #------------------------#
    # project/invoice creation
    #------------------------#

    def new_project_and_invoice(self, client_email, client_name, payment_link, project_link, invoice_link):

        contact_subject = "New Project in your Project Binder"

        text_swap = {
            '[CLIENT_NAME]': client_name,
            '[PAYMENT_LINK]': payment_link,
            '[PROJECT_LINK]': project_link,
            '[INVOICE_LINK]': invoice_link,
            }
        
        string = new_project_and_invoice
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

#### Test
"""test_send = os.getenv("TEST_SEND")

subject_test = "TEST"

body_test ="body"

SMTP = AutoReply()

SMTP.contact_request(test_send, 'john')
print('smtp request')
SMTP.contact_alart(test_send, 'john', subject_test, body_test)"""

