# apps/payments/views.py
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from apps.cauth.models import Tariff
from apps.cauth.serializers.tarif_serializer import TariffSerializer
from apps.cauth.permissions import AdminPermission


class TariffViewSet(viewsets.ModelViewSet):
    queryset = Tariff.objects.prefetch_related('translations__language').all()
    serializer_class = TariffSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            perm = [IsAuthenticated]
        else:
            perm = [AdminPermission]
        return [p() for p in perm]
