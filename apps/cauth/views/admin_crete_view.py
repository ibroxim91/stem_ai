# views.py

from rest_framework import generics
from apps.cauth.models import User
from apps.cauth.serializers import AdminCreateUserSerializer
from apps.cauth.permissions import AdminPermission

class AdminUserCreateView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = AdminCreateUserSerializer
    permission_classes = [AdminPermission]
