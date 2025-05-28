from rest_framework import generics, status
from rest_framework.response import Response
from apps.cauth.models import User
from apps.cauth.serializers.admin_serializer import AdminCreateUserSerializer
from apps.cauth.serializers.register_serializer import RegisterSerializer
from django.core.mail import send_mail
from django.conf import settings
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator
from rest_framework.permissions import AllowAny

from rest_framework.response import Response
from rest_framework import status

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer

    def perform_create(self, serializer):
        user = serializer.save()

        # Aktivatsiya havolasi
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        activation_link = f"{settings.FRONTEND_URL}/activate/{uid}/{token}"

        send_mail(
            subject="Verify your email",
            message=f"Click to activate your account: {activation_link}",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            fail_silently=False,
        )

        # Foydalanuvchini AdminCreateUserSerializer orqali serialize qilamiz
        serialized_user = AdminCreateUserSerializer(user).data

        # Return qilish uchun javobni saqlab qo'yamiz
        self._response_data = serialized_user  # keyinchalik response() dan qaytaramiz

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return Response(self._response_data, status=status.HTTP_201_CREATED)
