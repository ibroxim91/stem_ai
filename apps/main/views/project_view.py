from rest_framework import viewsets
from apps.main.models import ProjectCategory
from apps.main.serializers import ProjectCategorySerializer
from apps.cauth.permissions import AdminPermission
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from rest_framework.response import Response


class ProjectCategoryViewSet(viewsets.ModelViewSet):
    queryset = ProjectCategory.objects.all()#filter(parent_category__isnull=True)
    serializer_class = ProjectCategorySerializer

    def get_queryset(self):
        return super().get_queryset().prefetch_related('translations')
    
    def retrieve(self, request, *args, **kwargs):
        parent_project = get_object_or_404(ProjectCategory, id=kwargs.get('pk'))
        children = ProjectCategory.objects.filter(parent_category=parent_project)
        data = ProjectCategorySerializer(parent_project, many=False).data
        data['children'] = ProjectCategorySerializer(children, many=True).data
        return Response(data)
       

    def get_permissions(self):
        # Faqat create, update, partial_update, destroy uchun AdminPermission kerak
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [AdminPermission]
        else:
            # list va retrieve uchun oddiy IsAuthenticated yetarli
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
