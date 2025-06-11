# views.py

from rest_framework import generics
from apps.cauth.models import User
from apps.cauth.serializers import AdminCreateUserSerializer
from apps.cauth.permissions import AdminPermission
from drf_spectacular.utils import extend_schema

@extend_schema(summary="Admin qo'shish uchun", description="Admin qo'shish uchun")
class AdminUserCreateView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = AdminCreateUserSerializer
    permission_classes = [AdminPermission]
