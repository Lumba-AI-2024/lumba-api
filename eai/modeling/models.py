from django.db import models

# this model is records for modeling process
# status contains "accepted", "in progress",  "canceled", & "completed"
class ModelTrainingRecord(models.Model):
    status = models.CharField(max_length=100,default="accepted")
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)

class MLModel(models.Model):
    name = models.CharField(max_length=100, default='')
    file_name = models.CharField(max_length=100, default='')
    username = models.CharField(max_length=100, default="default")
    workspace = models.CharField(max_length=100, default="default")
    method = models.CharField(max_length=100, default="-")
    algorithm = models.CharField(max_length=100, default="-")
    metrics = models.CharField(max_length=100, default="-")
    score = models.FloatField(default=0)
    feature = models.TextField(blank=True)
    target = models.TextField(blank=True)
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)