from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiExample
from rest_framework import serializers

class TokenRefreshResponseSerializer(serializers.Serializer):
    access = serializers.CharField()

@extend_schema(
    summary="Tokenni yangilash",
    description="Refresh token yordamida yangi access token generatsiya qilish",
    request=TokenRefreshSerializer,
    responses={
        200: OpenApiResponse(
            response=TokenRefreshResponseSerializer,
            description="Yangi access token",
            examples=[
                OpenApiExample(
                    'Muvaffaqiyatli javob',
                    value={
                        "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                       
                    },
                    response_only=True,  # Bu muhim!
                    status_codes=['200']
                )
            ]
        ),
        400: OpenApiResponse(
            description="Noto'g'ri yoki muddati o'tgan refresh token",
           
        )
    }
)
class MyTokenRefreshView(TokenRefreshView):
    serializer_class = TokenRefreshSerializer