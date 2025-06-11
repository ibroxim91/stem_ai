from django.core.mail import send_mail
from django.conf import settings
from django.utils.crypto import get_random_string
from rest_framework import serializers
from apps.cauth.models import User
import threading

def send_password_reset_email(email, password):
    send_mail(
        "Parolni tiklash",
        f"Parolingiz o'zgartrildi yangi parolingiz: {password}",
        settings.DEFAULT_FROM_EMAIL,
        [email],
        fail_silently=False,
    )

class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    

    
    def save(self):
        email = self.validated_data['email']
        user = User.objects.get(email=email)
        
        # Token yaratish (yoki django-rest-passwordreset kutubxonasidan foydalaning)
        password = get_random_string(8)
        user.set_password(password)
        user.save()
        
        # Parolni emailga yuborish
        threading.Thread(target=send_password_reset_email, args=(email, password)).start()

