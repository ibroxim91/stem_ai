from rest_framework import generics, permissions
from apps.chat.models.chat_history import UserOpenAIChatHistory
from apps.chat.models.user_chat import UserChat
from drf_spectacular.utils import extend_schema, extend_schema_view
from drf_spectacular.types import OpenApiTypes
from apps.chat.serializers.chat_serializer import  UserMessageToPdfSerializer
from apps.chat.services.generate_pdf_service import  generate_wrapped_pdf
from apps.payme import Response
from django.http import FileResponse
import io
from reportlab.pdfgen import canvas


@extend_schema(
    tags=["Chat"],
    summary="Message to PDF",
    responses={200: OpenApiTypes.BYTE},  # Bu yerda 'application/pdf' avtomatik ko‘rsatiladi
)
class UserMessageToPdfView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        pk = kwargs['pk']
        instance = UserOpenAIChatHistory.objects.get(pk=pk)
        text = instance.response_text
        file = generate_wrapped_pdf(text=text)

        # PDF faylni stream ko‘rinishida qaytarish
        return FileResponse(
            file,
            as_attachment=True,
            filename=f"message_{pk}.pdf",
            content_type='application/pdf'
        )