from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions
from apps.main.models import QuestionGroup
from apps.main.models.project_category import ProjectCategory
from apps.main.serializers import QuestionGroupSerializer
from apps.main.serializers.project_serializer import ProjectCategorySerializer
from rest_framework.response import Response

class QuestionGroupsByCategoryView(generics.ListAPIView):
    serializer_class = QuestionGroupSerializer
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request, *args, **kwargs):
        print("list ", self.kwargs)
        parent_project = get_object_or_404(ProjectCategory, id=kwargs.get('id'))
    
        data = ProjectCategorySerializer(parent_project, many=False).data
        data['question_groups'] = QuestionGroupSerializer(self.get_queryset(), many=True).data
        return Response(data) 
    
    def get_queryset(self):
        category_id = self.kwargs.get('id')
        return QuestionGroup.objects.filter(category_id=category_id).prefetch_related('translations__language')
