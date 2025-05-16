from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from asgiref.sync import sync_to_async
from apps.main.models import ProjectCategory
from apps.main.serializers import ProjectCategorySerializer
from django.shortcuts import get_object_or_404

class ProjectCategoryDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        # get_object_or_404 ni sync_to_async bilan o'rash
        parent_project = get_object_or_404(ProjectCategory, id=id)

        children = ProjectCategory.objects.filter(parent_category=parent_project)
        print("children ", children)
        data = {
            'id': parent_project.id,
            
        }
        data['children'] = ProjectCategorySerializer(children, many=True).data
        return Response(data)
