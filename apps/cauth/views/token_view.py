from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiExample
from rest_framework import serializers

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Qo'shimcha claimlar qo'shish
        token['phone'] = user.phone
        token['first_name'] = user.first_name
        token['last_name'] = user.last_name
        token['is_superuser'] = user.is_superuser

        return token

class TokenObtainPairResponseSerializer(serializers.Serializer):
    access = serializers.CharField()
    refresh = serializers.CharField()


@extend_schema(
    summary="Token olish",
    description="Foydalanuvchi telefon raqami va paroli orqali access va refresh tokenlarni olish",
    request=CustomTokenObtainPairSerializer,
    responses={
        200: OpenApiResponse(
            response=TokenObtainPairResponseSerializer,
            description="Muvaffaqiyatli kirish",
            examples=[
                OpenApiExample(
                    'Muvaffaqiyatli javob',
                    value={
                        "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                        "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
                    },
                    response_only=True,  # Bu muhim!
                    status_codes=['200']
                )
            ]
        ),
        400: OpenApiResponse(
            description="Noto'g'ri so'rov yoki kirish ma'lumotlari",
            examples=[
                OpenApiExample(
                    'Noto\'g\'ri kirish ma\'lumotlari',
                    value={
                        "detail": "No active account found with the given credentials"
                    },
                    response_only=True,
                    status_codes=['400']
                )
            ]
        )
    }
)
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer