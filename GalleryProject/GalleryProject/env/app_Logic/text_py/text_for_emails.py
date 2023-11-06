

# contact forms emails -------------------------------------------------------------------------------

# auto reply to contact request

contact_request_body = """
Hi user_name,

Thank you for reaching out! I've received your message regarding user_subject, and I'll be sure to get back to you shortly.
I'm excited to discuss your photography needs and collaborate with you to create stunning visuals that capture your unique style.
In the meantime, please keep an eye on your inbox for my response. If you don't receive a follow-up email from me within 24 hours, 
please check your spam folder, just in case.

Looking forward to connecting with you soon!

Best regards,
Carly


SoftSubversion.com
"""

# contact form filled out 

contact_alart_body = """ 
        Subject: user_subject

        From: user_email - Name: user_name

        Message:
            body


"""

# client and project emails -------------------------------------------------------------------------------


# client requesing a new project 
project_request_notice_body = """

Project Request!!!
From: client_name - ID#: user_id
Project Name project_name
Requested Scope  scope
Requested date  date_selected
Requested Location type location
Details details
          
"""

# notice to clinet of new comment on project request

owner_post_comment_ = """
Hey user_name,

A new comment has been posted for your project reeequest project_name.

owner commented:

        comment

link


"""
owner_post_comment_body = str(owner_post_comment_)


send_invite_text = """

Dear [client_name],

We're thrilled to extend an exclusive invitation for you to become a part of Soft Subversion's Online Studio, where you'll gain access to a world of captivating photography and personalized experiences.

To kickstart your journey with us and unlock the ability to submit project requests, you'll need to complete your registration by creating an account. To begin, please make note of your unique registration key: [REG_KEY]. Then, follow this link to register using your exclusive key:

[REG_URL]

Here's a brief overview of what you can anticipate from your Soft Subversion's Online Studio account:
Seamless Project Requests: You'll be able to submit project requests and directly collaborate with Carly to outline project details, ensuring your vision comes to life.


Private Proofing Gallery: Gain access to a private gallery where you can preview your photos for proofing purposes. Feel free to communicate directly with Carly to fine-tune your selections before finalization.


Easy Downloads and Printing: Once your final payment is processed, you'll have the convenience of downloading high-quality copies of your gallery and even ordering prints directly from Soft Subversion's Online Studio.


Should you encounter any questions or encounter any hiccups during the registration process, our dedicated support team is here to provide assistance. Reach out to us at support@softsubversion.com, and we'll guide you through any challenges you may face.
Thank you for choosing to embark on this creative journey with us at Soft Subversion's Online Studio. We look forward to helping you bring your photography and videography projects to life.

Warm regards,

Carley Brown
Photographer/Videographer 
Soft Subversion 
Website: softsubversion.com  
Email: Carly@softsubversion.com"""

# client requesing a new project 
new_project_and_invoice = """

Dear [CLIENT_NAME],

I hope this message finds you well. I am excited to inform you that a new project has been approved and is now available in your Project Binder.

Project Details:
- Project Name: [PROJECT_NAME]
- Invoice Number: [INVOICE_NUMBER]
- Due Date: [DUE_DATE]

To ensure a smooth process, please take the following actions:
1. Click on the following link to view the project details: [PROJECT_LINK]
2. Review the project scope and details carefully.
3. To make a payment or view the invoice, click here: [PAYMENT_LINK]
4. Please make sure to complete the payment by the due date ([DUE_DATE]). Failure to do so may result in project cancellation.

If you have any questions or require further assistance, please don't hesitate to contact me.

Thank you for choosing Soft Subversion for your photography needs. I look forward to working with you on this exciting project!


Carley Brown
Photographer/Videographer 
Soft Subversion 
Website: softsubversion.com  
Email: Carly@softsubversion.com"""