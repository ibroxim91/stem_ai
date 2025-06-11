from rest_framework import generics
from apps.cauth.serializers.password_reset_serializer import PasswordResetRequestSerializer
from drf_spectacular.utils import extend_schema
from rest_framework.response import Response
from rest_framework import status
from rest_framework import serializers
from apps.cauth.models import User


class PasswordResetSuccessResponseSerializer(serializers.Serializer):
    detail = serializers.CharField( default="Yangi Parol  emailga yuborildi")


class PasswordResetErrorResponseSerializer(serializers.Serializer):
    detail = serializers.CharField( default="Ushbu email bilan ro'yxatdan o'tgan foydalanuvchi topilmadi")


@extend_schema(
    summary="Parolni yangilash",
    description="Agar yuborilgan email mavjud bo'lsa user uchun o'rnatilgan yangi  parol emailga yuboriladi",
    request=PasswordResetRequestSerializer,
        responses={
            200: PasswordResetSuccessResponseSerializer,
            400: PasswordResetErrorResponseSerializer
        } 
   
)
class PasswordResetRequestView(generics.CreateAPIView):
    serializer_class = PasswordResetRequestSerializer
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        email = data['email']
        user = User.objects.filter(email=email).first()
        if not user:
            return Response(
                {"detail": "Ushbu email bilan ro'yxatdan o'tgan foydalanuvchi topilmadi"},
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer.save()
        return Response(
            {"detail": "Yangi Parol  emailga yuborildi"},
            status=status.HTTP_200_OK
        )
