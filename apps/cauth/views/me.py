from rest_framework.views  import APIView
from rest_framework.permissions import IsAuthenticated
from apps.cauth.models import User
from apps.cauth.serializers.admin_serializer import AdminCreateUserSerializer
from rest_framework.response import Response

class MeUserView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user = request.user
        serializer = AdminCreateUserSerializer(user, many=False)
        return Response(serializer.data)
        
