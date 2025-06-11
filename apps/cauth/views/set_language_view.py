from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from apps.main.models import Language
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import serializers

class SetLanguageResponseSerializer(serializers.Serializer):
    message = serializers.CharField(default='Language set successfully')


@extend_schema(request=None, summary="Til o'rnatish",  responses={201: SetLanguageResponseSerializer})
class SetLanguageView(APIView):
    permission_classes = [IsAuthenticated]
    @extend_schema(
        parameters=[
            OpenApiParameter(
                name='language_id',
                description='Language id',
                location=OpenApiParameter.QUERY,
                required=True,
                type=int
            ),
        ],
       )        
    def get(self, request):
        language_id = request.GET.get('language_id')
        if not Language.objects.filter(id=language_id).exists():
            return Response({'error': 'Invalid language id'}, status=status.HTTP_400_BAD_REQUEST)
        language = Language.objects.get(id=language_id)
        request.user.language = language
        request.user.save()
        return Response({'message': 'Language set successfully'}, status=status.HTTP_200_OK)