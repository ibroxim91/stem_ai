# views.py

from rest_framework import viewsets
from apps.main.models import Language
from apps.main.serializers import LanguageSerializer
from rest_framework.permissions import IsAuthenticated


class LanguageViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Language.objects.all()
    serializer_class = LanguageSerializer
