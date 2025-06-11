from rest_framework import viewsets
from apps.main.models import ProjectCategory
from apps.main.paginator import StandardResultsSetPagination, get_paginated_response_schema
from apps.main.serializers import ProjectCategorySerializer
from apps.cauth.permissions import AdminPermission
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter


@extend_schema(
    tags=["Kategoriyalar"],
    description="Kategoriyalar ro'yxati",
   
)
@extend_schema_view(
    list=extend_schema(
        summary="Kategoriyalar ro'yxati",
        description="Barcha mavjud Kategoriyalarni paginatsiya bilan qaytaradi",    
    ),
    create=extend_schema(
        summary="Kategoriya qo'shish (Admin)",
        description="Faqat adminlar yangi Kategoriya qo'shishi mumkin"
    ),
    retrieve=extend_schema(
        summary="Kategoriyani ko'rish",
        description="Kategoriya ID si orqali bitta Kategoriyani ko'rish"
    ),
    update=extend_schema(
        summary="Kategoriyani to'liq yangilash (Admin)",
        description="Faqat adminlar Kategoriya ma'lumotlarini to'liq yangilashi mumkin"
    ),
    partial_update=extend_schema(
        summary="Kategoriyani qisman yangilash (Admin)",
        description="Faqat adminlar Kategoriya ma'lumotlarini qisman yangilashi mumkin"
    ),
    destroy=extend_schema(
        summary="Kategoriyani o'chirish (Admin)",
        description="Faqat adminlar Kategoriyani o'chirishi mumkin"
    ),
)
class ProjectCategoryViewSet(viewsets.ModelViewSet):
    queryset = ProjectCategory.objects.all()#filter(parent_category__isnull=True)
    serializer_class = ProjectCategorySerializer
    pagination_class = StandardResultsSetPagination


    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
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
