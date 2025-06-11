from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework import status
from apps.cauth.serializers.password_change_serializer import ChangePasswordSerializer
from drf_spectacular.utils import extend_schema
from rest_framework import serializers

class PasswordChangeResponseSerializer(serializers.Serializer):
    detail = serializers.CharField( default="Parol muvaffaqiyatli o'zgartirildi")


@extend_schema(summary="Parolni o'zgartirish", request=ChangePasswordSerializer, responses={200: PasswordChangeResponseSerializer})
class ChangePasswordView(generics.UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        return self.request.user
    
    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user = self.get_object()
        user.set_password(serializer.validated_data['new_password'])
        user.save()
        
        return Response(
            {"detail": "Parol muvaffaqiyatli o'zgartirildi"},
            status=status.HTTP_200_OK
        )