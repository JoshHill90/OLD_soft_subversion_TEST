from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
import secrets
import random
import datetime


class Dispaly(models.Model):
    name = models.CharField(max_length=255)
    def __str__(self):
        return str(self.id) + ' | ' + str(self.name)



class Image(models.Model):
    title = models.CharField(max_length=255)
    date = models.DateField(auto_now_add=True)
    tag = models.CharField(max_length=255)
    portrait_format = models.CharField(max_length=50, default='square')
    private = models.BooleanField(default=False)
    display = models.ManyToManyField(Dispaly, blank=True, null=True)
    client_id = models.ForeignKey('client.Client', null=True, blank=True, on_delete=models.SET_NULL)
    project_id = models.ForeignKey('client.Project', null=True, blank=True, on_delete=models.SET_NULL)
    image_link = models.URLField(blank=True, default=' ')
    cloudflare_id = models.CharField(max_length=255, blank=True)
    silk_id = models.CharField(max_length=50, default='CB01')

    def __str__(self):
        return str(self.title)

    def get_absolute_url(self):
        return reverse("image-details", kwargs={"slug": self.cloudflare_id})