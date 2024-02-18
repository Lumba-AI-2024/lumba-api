import json
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import pandas as pd
from file.serializers import FileSerializer
from data_science.preprocess import Preprocess
import os
import string
import random

@api_view()
def cleaning_handler(request):
    try:
        file_name = request.query_params['filename']
        username = request.query_params['username']
        workspace = request.query_params['workspace']
    except:
        return Response({'message': "input error"},status=status.HTTP_400_BAD_REQUEST)
    
    current_path = os.getcwd()
    save_path = f'{current_path}/directory/{username}/{workspace}/{file_name}'
    dataframe = pd.read_csv(save_path)
    preprocess = Preprocess(dataframe=dataframe)
    
    if request.query_params['missing'] == '1':
        if request.query_params['columns_missing'] != '':
            col = request.query_params['columns_missing'].split(",")
            preprocess.data_null_handler(col)
        else:
            preprocess.data_null_handler()

    if request.query_params['duplication'] == '1':
        if request.query_params['columns_duplication'] != '':
            col = request.query_params['columns_duplication'].split(",")
            preprocess.data_duplication_handler(col)
        else:
            preprocess.data_duplication_handler()

    if request.query_params['outlier'] == '1':
        preprocess.data_outlier_handler()

    # generate new file name
    new_file_name = generate_file_name(file_name)
    
    # save cleaned dataset to csv
    save_path = f'{current_path}/directory/{username}/{workspace}/{new_file_name}'    
    if os.path.isfile(save_path):
        return Response({'errcode': "input error", 'message':"file name must unique"},status=status.HTTP_400_BAD_REQUEST)
    preprocess.dataframe.to_csv(save_path)

    # create new file model with serializer
    file_size = round(os.path.getsize(save_path)/(1024 * 1024), 2)

    # check and collect columns type
    columns_type = preprocess.get_all_column_type()
    numeric_type = []
    non_numeric_type = []
    for k,v in columns_type.items():
        if v in ['Numerical']:
            numeric_type.append(k)
        else:
            non_numeric_type.append(k)
    numeric = ''
    non_numeric = ''
    if not len(numeric_type) == 0:
        numeric = ','.join(numeric_type)
    if not len(non_numeric_type) == 0:
        non_numeric_type = ','.join(non_numeric_type)

    payload = {
            'file' : new_file_name,
            'size': file_size,
            'username' : username,
            'workspace' : workspace,
            'numeric' : numeric,
            'non_numeric' : non_numeric,
        }
    file_serializer = FileSerializer(data=payload)   
    if not file_serializer.is_valid():
        os.remove(save_path)
        return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # save file model to database
    file_serializer.save()

    return Response(json.loads(preprocess.dataframe.head(10).to_json()), status=status.HTTP_200_OK)

def generate_file_name(file_name):
    file, ext = os.path.splitext(file_name)
    new_file_name = file + "_" + random_string() + ext
    return new_file_name

def random_string(length=4):
    return ''.join(random.choice(string.ascii_letters) for _ in range(length))