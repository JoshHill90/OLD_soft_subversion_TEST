from django.contrib import admin
from .models import Contact
from gallery.models import Image
#from blog.models import Blog
from user_system.models import credit, Coupon, Invoice, LineItem
from client.models import Client, Project, ProjectEvents, ProjectRequest, RequestReply, ProjectTerms, Invite

#admin.site.register(Blog)
admin.site.register(Project)
admin.site.register(Image)
admin.site.register(Contact)
admin.site.register(Coupon)
admin.site.register(credit)
admin.site.register(Client)
admin.site.register(Invite)
#admin.site.register(Print)
admin.site.register(Invoice)
admin.site.register(LineItem)
admin.site.register(ProjectRequest)
admin.site.register(RequestReply)
admin.site.register(ProjectTerms)
admin.site.register(ProjectEvents)
