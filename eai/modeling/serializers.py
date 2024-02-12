from rest_framework import serializers
from .models import ModelTrainingRecord, MLModel

class ModelTrainingRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = ModelTrainingRecord
        fields = ('id', 'status', 'created_time', 'updated_time')

class MLModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = MLModel
        fields = ('name', 'file_name', 'username', 'workspace', 'method', 'algorithm', 'metrics', 'score', 'feature', 'target', 'created_time', 'updated_time')