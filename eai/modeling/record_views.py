import json
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import ModelTrainingRecord
from .serializers import ModelTrainingRecordSerializer

def create_training_record(request):
    payload = json.loads(request.body)
    modeltrainingrecord_serializer = ModelTrainingRecordSerializer(data=payload)
    if modeltrainingrecord_serializer.is_valid():
        modeltrainingrecord_serializer.save()
        return JsonResponse(modeltrainingrecord_serializer.data)
    
    return JsonResponse(modeltrainingrecord_serializer.errors)

def update_training_record(request):
    payload = json.loads(request.body)
    training_record = ModelTrainingRecord.objects.get(id=payload['id'])
    modeltrainingrecord_serializer = ModelTrainingRecordSerializer(training_record,data=payload)
    if modeltrainingrecord_serializer.is_valid():
        modeltrainingrecord_serializer.save()
        return JsonResponse(modeltrainingrecord_serializer.data)
    
    return JsonResponse(modeltrainingrecord_serializer.errors)

@api_view()
def get_training_record(request):
    try:
        training_record = ModelTrainingRecord.objects.get(id=request.query_params['id'])
    except:
        return Response({'message': "data not found"}, status=status.HTTP_404_NOT_FOUND)
    trainingrecord_serializer = ModelTrainingRecordSerializer(training_record)
    return Response(trainingrecord_serializer.data, status=status.HTTP_200_OK)