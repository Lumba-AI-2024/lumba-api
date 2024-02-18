import os
import joblib
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import numpy as np
import pandas as pd

@api_view()
def model_do_predict(request):
    try:
        model_name = request.query_params['modelname']
        feature = int(request.query_params['feature'])
    except:
        return Response({'message': "input error"},status=status.HTTP_400_BAD_REQUEST)

    current_path = os.getcwd()
    model_path = f'{current_path}/directory/default/default/{model_name}'
    model = joblib.load(model_path)
    predict = model.predict(np.array([feature]).reshape(-1,1))
 
    return Response({'result': predict[0][0]}, status=status.HTTP_200_OK)