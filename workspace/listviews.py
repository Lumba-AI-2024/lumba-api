from rest_framework.views import APIView
from .serializers import WorkspaceSerializer
from rest_framework.response import Response
from rest_framework import status
from .models import Workspace

class ListWorkspaceView(APIView):
    def get(self, request, *args, **kwargs):
        workspaces = Workspace.objects.all()
        workspaces_serializer = WorkspaceSerializer(workspaces, many=True)
        return Response(workspaces_serializer.data, status=status.HTTP_200_OK)