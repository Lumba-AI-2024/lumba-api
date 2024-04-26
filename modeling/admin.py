from django.contrib import admin

from modeling.models import ModelTrainingRecord, MLModel

# Register your models here.
admin.site.register(ModelTrainingRecord)
admin.site.register(MLModel)