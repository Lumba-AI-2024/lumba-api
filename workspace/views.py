from datetime import datetime
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import WorkspaceSerializer
from .models import Workspace

class WorkspaceView(APIView):
    def post(self, request, *args, **kwargs):
        # manual parsing the request
        try:
            name = request.data['name']
            username = request.data['username']
            description = request.data['description']
        except:
            return Response({'message': "input error"},status=status.HTTP_400_BAD_REQUEST)

        payload = {
            'name' : name,
            'username' : username,
            'description' : description,
        }
        workspace_serializer = WorkspaceSerializer(data=payload)
       
        if workspace_serializer.is_valid():
            if Workspace.objects.filter(name=name).exists() :
                return Response({'message': "already exist"},status=status.HTTP_400_BAD_REQUEST)
            workspace_serializer.save()
            return Response(workspace_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(workspace_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request, *args, **kwargs):
        try:
            workspace = Workspace.objects.get(name=request.query_params['name'])
        except:
            return Response({'message': "data not found"}, status=status.HTTP_404_NOT_FOUND)
        workspace_serializer = WorkspaceSerializer(workspace)
        return Response(workspace_serializer.data, status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        try:
            workspace = Workspace.objects.get(name=request.query_params['name'])
        except:
            return Response({'message': "data not found"}, status=status.HTTP_404_NOT_FOUND)

        payload = {
            'name' : request.data['name'],
            'username' : request.data['username'],
            'description' : request.data['description'],
        }
        workspace_serializer = WorkspaceSerializer(workspace, data=payload)
        if workspace_serializer.is_valid():
            workspace_serializer.save()
            return Response(workspace_serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(workspace_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, *args, **kwargs):
        try:
            workspace = Workspace.objects.get(name=request.data['name'])
        except:
            return Response({'message': "data not found"}, status=status.HTTP_404_NOT_FOUND)
        workspace.delete()
        return Response({'message': "deleted successfully"},status=status.HTTP_204_NO_CONTENT)