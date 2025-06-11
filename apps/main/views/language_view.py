# views.py

from rest_framework import viewsets
from apps.main.models import Language
from apps.main.serializers import LanguageSerializer
from apps.cauth.permissions import AdminPermission
from rest_framework.permissions import  AllowAny


class LanguageViewSet(viewsets.ModelViewSet):
    permission_classes = [AdminPermission]
    queryset = Language.objects.all()
    serializer_class = LanguageSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [AdminPermission]
        else:
            permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]
