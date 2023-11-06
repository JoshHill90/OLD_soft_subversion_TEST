from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from GalleryProject.env.app_Logic.untility.quick_tools import DateFunction
df = DateFunction()

class Client(models.Model):
    name = models.CharField(max_length=255)
    strip_id = models.CharField(max_length=255, null=True, blank=True)
    phone = models.CharField(max_length=10, verbose_name='Contact Phone Number')
    email = models.EmailField(max_length=100, verbose_name='Email Address')
    address_1 = models.CharField(max_length=255, verbose_name='Street Address/PO Box')
    address_2 = models.CharField(max_length=255, verbose_name='Apt/Suite')
    city = models.CharField(max_length=255, verbose_name='City')
    state = models.CharField(max_length=255, verbose_name='State')
    zip_code =models.CharField(max_length=255, verbose_name='Zipcode')
    user_id = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return str(self.name)

    def get_absolute_url(self):
        return reverse("client-details", args=(self.id))

class Project(models.Model):
    name = models.CharField(max_length=255)
    status = models.CharField(max_length=255, default='Pending Deposit')
    client_id = models.ForeignKey(Client, null=True, blank=True, on_delete=models.SET_NULL)
    slug = models.SlugField(null=False, unique=True)

    def __str__(self):
        return str(self.name)

    def get_absolute_url(self):
        return reverse("project-details", kwargs={"slug": self.slug})
    
class Invite(models.Model):
    name = models.CharField(max_length=255, verbose_name='Name')
    email = models.EmailField(max_length=100, verbose_name='Email Address' )
    hexkey = models.CharField(max_length=32)
    used = models.BooleanField(default=False)

    def __str__(self):
        return str(self.name)

    def get_absolute_url(self):
        return reverse("project-binder", args=(str(self.id)))
    
    
class ProjectRequest(models.Model):
    name = models.CharField(max_length=255, verbose_name='Project Name')
    user_id = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    date = models.CharField(max_length=10)
    scope = models.CharField(max_length=255, verbose_name='Project-Type/Scope')
    details = models.CharField(max_length=3000, verbose_name='Project Details')
    slug = models.SlugField(null=False, unique=True, max_length=32)
    location = models.CharField(max_length=255, verbose_name='Location type')
    status = models.CharField(max_length=25, default='pending')

    def __str__(self):
        return str(self.name)

    def get_absolute_url(self):
        
        return reverse("request-status", args=(str(self.id)))
    
class RequestReply(models.Model):
    project_request_id = models.ForeignKey(ProjectRequest, null=True, blank=True, on_delete=models.SET_NULL)
    user_id = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    comment = models.CharField(max_length=3000)
    date_posted = models.DateField(auto_now=True)
    read = models.BooleanField(default=False)

    def __str__(self):
        return str(self.project_request_id) + ' | ' + str(self.user_id)

    def get_absolute_url(self):
        
        return reverse("request-status", kwargs={"slug": self.slug})
    
class ProjectTerms(models.Model):
    project_request_id = models.ForeignKey(ProjectRequest, null=True, blank=True, on_delete=models.SET_NULL)
    project_id = models.ForeignKey(Project, null=True, blank=True, on_delete=models.SET_NULL)
    user_id = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    scope = models.CharField(max_length=255)
    services = models.TextField(max_length=5000, blank=True)
    project_cost = models.FloatField(default='600.00')
    deposit = models.FloatField(default='0.00')
    project_docs = models.CharField(max_length=255)

    def __str__(self):
        return str(self.project_request_id) + ' | ' + str(self.user_id)

    def get_absolute_url(self):
        
        return reverse("request-approval", args=(str(self.id)))
    
    
class ProjectEvents(models.Model):
    title = models.CharField(max_length=255)
    billing_id = models.ForeignKey('user_system.Invoice', null=True, blank=True, on_delete=models.SET_NULL)
    project_id = models.ForeignKey(Project, null=True, blank=True, on_delete=models.SET_NULL)
    date = models.DateField(auto_now=True)
    start = models.TimeField(blank=True, null=True)
    end = models.TimeField(blank=True, null=True)
    event_type = models.CharField(max_length=50, blank=True)
    details = models.CharField(max_length=500, blank=True)

    
    def __str__(self):
        return str(self.title)

    def get_absolute_url(self):
        date = df.date_now()
        year, month, day = date.split('-')
        return reverse("project-calendar", args=(year, month))
    
class Note(models.Model):
    project_id = models.ForeignKey(Project, null=True, blank=True, on_delete=models.SET_NULL)
    user_id = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    note = models.TextField(max_length=3000)
    date_posted = models.DateField(auto_now=True)

    def __str__(self):
        return str(self.id)

    def get_absolute_url(self):
        
        return reverse("project-notes", args=(str(self.project_id)))