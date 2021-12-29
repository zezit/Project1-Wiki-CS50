from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
from django.urls import reverse

# Create your models here.

class Post(models.Model):
    title = models.CharField(max_length=255)
    body = RichTextField(blank=True, null=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('entry', args=(str(self.title)))
