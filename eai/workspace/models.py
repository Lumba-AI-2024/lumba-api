from django.db import models
from django.utils import timezone

class Workspace(models.Model):
    name = models.CharField(max_length=100, blank=False, null=False)
    username = models.CharField(max_length=100, default="default")
    description = models.CharField(max_length=200, default="default")
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)