from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
import secrets
import random
import datetime

DISPLAY_PEACE = [    
    ('none', 'none'),
    ('home', 'home'),
    ('IOTM', 'IOTM'),
    ('model', 'model'),
    ('wedding', 'wedding'),
    ('family', 'family'),
    ('modelgal', 'modelgal'),
    ('weddinggal', 'weddinggal'),
    ('familygal', 'familygal'),
    ('project', 'project'),
    ('project-header', 'project-header'),
]

class Image(models.Model):
    title = models.CharField(max_length=255)
    date = models.DateField(auto_now_add=True)
    tag = models.CharField(max_length=255)
    portrait_format = models.CharField(max_length=50, default='square')
    private = models.BooleanField(default=False)
    display = models.CharField(max_length=20, choices=DISPLAY_PEACE, default='none')
    client_id = models.ForeignKey('client.Client', null=True, blank=True, on_delete=models.SET_NULL)
    project_id = models.ForeignKey('client.Project', null=True, blank=True, on_delete=models.SET_NULL)
    image_link = models.URLField(blank=True, default=' ')
    cloudflare_id = models.CharField(max_length=255, blank=True)
    silk_id = models.CharField(max_length=50, default='CB01')

    def __str__(self):
        return str(self.title)

    def get_absolute_url(self):
        return reverse("image-details", kwargs={"slug": self.cloudflare_id})