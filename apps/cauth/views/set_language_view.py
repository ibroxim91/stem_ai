from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from apps.main.models import Language



class SetLanguageView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        language_id = request.GET.get('language_id')
        if not Language.objects.filter(id=language_id).exists():
            return Response({'error': 'Invalid language id'}, status=status.HTTP_400_BAD_REQUEST)
        language = Language.objects.get(id=language_id)
        request.user.language = language
        request.user.save()
        return Response({'message': 'Language set successfully'}, status=status.HTTP_200_OK)