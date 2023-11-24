from django.contrib import admin
from .models import Contact, Document
from gallery.models import Image, Dispaly
#from blog.models import Blog
from user_system.models import credit, Coupon, Invoice, LineItem
from client.models import Client, Project, ProjectEvents, ProjectRequest, RequestReply, ProjectTerms, Invite, Note

#admin.site.register(Blog)
admin.site.register(Project)
admin.site.register(Image)
admin.site.register(Contact)
admin.site.register(Coupon)
admin.site.register(credit)
admin.site.register(Client)
admin.site.register(Invite)
admin.site.register(Note)
admin.site.register(Dispaly)
admin.site.register(Invoice)
admin.site.register(LineItem)
admin.site.register(Document)
admin.site.register(ProjectRequest)
admin.site.register(RequestReply)
admin.site.register(ProjectTerms)
admin.site.register(ProjectEvents)
