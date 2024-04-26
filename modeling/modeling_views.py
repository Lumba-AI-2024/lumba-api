import os
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
import requests
from .models import MLModel
from .serializers import MLModelSerializer
from file.models import File

# accept request from user
# passing params to service
@api_view(['POST'])
def initiate_modeling(request):
    try:
        model_name = request.data['modelname']
        file_name = request.data['filename']
        username = request.data['username']
        workspace = request.data['workspace']
        method = request.data['method']
        algorithm = request.data['algorithm']
        feature = request.data['feature']
        target = request.data['target']
    except:
        return Response({'message': "input error"},status=status.HTTP_400_BAD_REQUEST)
    
    # setup request to training service endpoint
    training_service_url = 'http://127.0.0.1:7000/train/'
    current_path = os.getcwd()
    file_path = f'{current_path}/directory/{username}/{workspace}/{file_name}'
    files = {'file': open(file_path, 'rb')}
    model_metadata = {
            'model_name': model_name,
            'file_name' : file_name,
            'username' : username,
            'workspace' : workspace,
            'method' : method,
            'algorithm' : algorithm,
            'feature' : feature,
            'target' : target,
    }
    training_record = requests.post(training_service_url, data=model_metadata, files=files)
    
    return Response(data=training_record.json(), status=status.HTTP_202_ACCEPTED)

def save_model(request):
    # fetch request file & model metadata
    model_metadata = request.POST.dict()
    files = request.FILES['file']

    # fetch model metadata
    model_name = f"{model_metadata['model_name']}.pkl"
    file_name = model_metadata['file_name']
    username = model_metadata['username']
    workspace = model_metadata['workspace']
    method = model_metadata['method']
    algorithm = model_metadata['algorithm']
    metrics = model_metadata['metrics']
    score = model_metadata['score']
    feature = model_metadata['feature']
    target = model_metadata['target']

    payload = {
        'name' : model_name,
        'file_name' : file_name,
        'username': username,
        'workspace' : workspace,
        'method' : method,
        'algorithm' : algorithm,
        'metrics' : metrics,
        'score' : score,
        'feature' : feature,
        'target' : target,
    }
    mlmodel_serializer = MLModelSerializer(data=payload)

    if mlmodel_serializer.is_valid():
        # configure save_path then save model to directory
        current_path = os.getcwd()
        save_path = f'{current_path}/directory/{username}/{workspace}/{model_name}'
        with open(f'{save_path}', 'wb') as destination:
                for chunk in files.chunks():
                    destination.write(chunk)
        # save model to db
        mlmodel_serializer.save()
        return JsonResponse(mlmodel_serializer.data)

    return JsonResponse(mlmodel_serializer.errors)

@api_view()
def list_model(request):
    mmlmodels = MLModel.objects.all()
    mlmodel_serializer = MLModelSerializer(mmlmodels, many=True)
    return Response(mlmodel_serializer.data, status=status.HTTP_200_OK)

@api_view()
def get_columns_type_by_modeling_method(request):
    try:
        file_name = request.query_params['filename']
        username = request.query_params['username']
        workspace = request.query_params['workspace']
        method = request.query_params['method']
    except:
        return Response({'message': "input error"}, status=status.HTTP_400_BAD_REQUEST)

    file = File.objects.get(file=file_name, username=username, workspace=workspace)
    columns = []
    if method == "REGRESSION":
        columns = file.numeric.split(",")
    if method == "CLASSIFICATION":
        columns = file.numeric.split(",")

    response = {
        'columns' : columns
    }
    return Response(response, status=status.HTTP_200_OK)
