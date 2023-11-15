from django.db import models
from django.urls import reverse

doc_type_choice = [
    ('site', 'site'),
    ('client', 'client'),
]
doc_kind = [
    ('pdf', 'pdf'),
    ('docx', 'docx'),
    ]

#-------------------------------------------------------------------------------------------------------#
# models class
#-------------------------------------------------------------------------------------------------------#

class Contact(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=255)
    subject = models.CharField(max_length=255)
    body = models.TextField(max_length=800)

    def __str__(self):
        return f'Name: {self.name} - Subject: {self.subject}'
    
    def get_absolute_url(self):
        return reverse("contact-success")
    
class Document(models.Model):
    name = models.CharField(max_length=50)
    file_path = models.CharField(max_length=255, null=True, blank=True)
    doc_type = models.CharField(choices=doc_type_choice, null=True, blank=True, max_length=50)
    doc_content = models.TextField(max_length=None, blank=True, null=True)
    modified = models.DateTimeField(auto_now=True)
    kind = models.CharField(choices=doc_kind, null=True, blank=True, max_length=50)
    created = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return str(self.name)
    
    def get_absolute_url(self):
        return reverse("o-documnents")