
import docx
from pathlib import Path

current_dir = Path(__file__).resolve().parent
ven = current_dir / "../.." / ".env"

def readtxt(doc):
    fullText = []
    for para in doc.paragraphs:
        fullText.append(para.text)
    return '\n'.join(fullText)  

# contact forms emails -------------------------------------------------------------------------------

# auto reply to contact request
contact_request_body_doc = docx.Document('static/documents/docx/contact_request_body.docx')
contact_request_body = readtxt(contact_request_body_doc)

# contact form filled out 
contact_alart_body_doc = docx.Document('static/documents/docx/contact_alart_body.docx')
contact_alart_body = readtxt(contact_alart_body_doc)
# client and project emails -------------------------------------------------------------------------------

# client requesing a new project 
project_request_notice_body_doc = docx.Document('static/documents/docx/project_request_notice_body.docx')
project_request_notice_body = readtxt(project_request_notice_body_doc)

# notice to clinet of new comment on project request
request_post_comment_doc = docx.Document('static/documents/docx/request_post_comment.docx')
request_post_comment = readtxt(request_post_comment_doc)

send_invite_text_doc = docx.Document('static/documents/docx/send_invite_text.docx')
send_invite_text = readtxt(send_invite_text_doc) 

# Approved new project with deposit invoice 
new_project_and_invoice_doc = docx.Document('static/documents/docx/new_project_and_invoice.docx')
new_project_and_invoice = readtxt(new_project_and_invoice_doc)

# Approved project without deposit invoice 
new_project_no_invoice_doc = docx.Document('static/documents/docx/new_project_no_invoice.docx')
new_project_no_invoice = readtxt(new_project_no_invoice_doc)   

# New invoice 
new_invoice_doc = docx.Document('static/documents/docx/new_invoice.docx')
new_project_no_invoice = readtxt(new_invoice_doc)   

# Resend invoice 
resend_invoice_doc = docx.Document('static/documents/docx/resend_invoice.docx')
resend_invoice = readtxt(resend_invoice_doc)   