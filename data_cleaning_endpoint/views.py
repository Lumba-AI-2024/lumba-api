import json
import os

import requests
from rest_framework import status

from rest_framework.decorators import api_view
from rest_framework.response import Response

from file.serializers import FileSerializer

preproc_url = 'http://127.0.0.1:5000/'


@api_view()
def master_handler(request, feat):
	if feat != "handle":
		response = requests.get(f"{preproc_url}/{feat}", params=request.query_params)
		return Response(response.json())
	else:
		response = requests.get(f"{preproc_url}/handle", params=request.query_params)
		"""
		response should return the following data:
		payload = {
			'file' : new_file_name,
			'size': file_size,
			'username' : username,
			'workspace' : workspace,
			'numeric' : numeric,
			'non_numeric' : non_numeric,
			}
		"""

		file_serializer = FileSerializer(data=response.json())
		if not file_serializer.is_valid():
			return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

		# save file model to database
		file_serializer.save()

		# TODO: return the first 10 lines of the preprocessed lines

		return Response(({'dummy': "this should return the first 10 lines"}), status=status.HTTP_200_OK)
