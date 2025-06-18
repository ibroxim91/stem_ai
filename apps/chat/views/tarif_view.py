# apps/payments/views.py
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from apps.cauth.models import Tariff
from apps.cauth.serializers.tarif_serializer import TariffSerializer
from apps.cauth.permissions import AdminPermission
from drf_spectacular.utils import extend_schema, extend_schema_view
model_name = "Tarif"
plural_name = model_name + 'lar' 


@extend_schema(tags=["Tariflar"])   
@extend_schema_view(
        list=extend_schema(
            summary=f"{plural_name} ro'yxati",
            description=f"Barcha mavjud {plural_name}ni paginatsiya bilan qaytaradi"
        ),
        create=extend_schema(
            summary=f"{model_name} qo'shish (Admin)",
            description=f"Adminlar yangi {model_name} qo'shishi mumkin"
        ),
        retrieve=extend_schema(
            summary=f"{model_name}ni ko'rish",
            description=f"{model_name} ID si orqali bitta {model_name}ni ko'rish"
        ),
        update=extend_schema(
            summary=f"{model_name}ni to'liq yangilash (Admin)",
            description=(f"Adminlar {model_name} ma'lumotlarini to'liq yangilashi mumkin")
        ),
        partial_update=extend_schema(
            summary=f"{model_name}ni qisman yangilash (Admin)",
            description=(f"Adminlar {model_name} ma'lumotlarini qisman yangilashi mumkin")
        ),
        destroy=extend_schema(
            summary=f"{model_name}ni o'chirish (Admin)",
            description=(f"Adminlar {model_name}ni o'chirishi mumkin")
        ),
    )
class TariffViewSet(viewsets.ModelViewSet):
    queryset = Tariff.objects.prefetch_related('translations__language').all()
    serializer_class = TariffSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            perm = [IsAuthenticated]
        else:
            perm = [AdminPermission]
        return [p() for p in perm]
