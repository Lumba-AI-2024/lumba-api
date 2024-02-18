from rest_framework.views import APIView
from .serializers import FileSerializer
from rest_framework.response import Response
from rest_framework import status
from .models import File

class ListFileView(APIView):
    def get(self, request, *args, **kwargs):
        try:
            username = request.query_params['username']
            workspace = request.query_params['workspace']
        except:
            return Response({'message': "input error"},status=status.HTTP_400_BAD_REQUEST)

        files = File.objects.filter(username=username, workspace=workspace)
        files_serializer = FileSerializer(files, many=True)
        return Response(files_serializer.data, status=status.HTTP_200_OK)