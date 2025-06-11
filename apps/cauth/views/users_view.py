from rest_framework.views  import APIView
from rest_framework.permissions import IsAuthenticated
from apps.cauth.models import User
from apps.cauth.serializers.admin_serializer import AdminCreateUserSerializer
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from apps.cauth.permissions import AdminPermission
from drf_spectacular.utils import extend_schema


@extend_schema(request=None, summary="Userlarni ko'rish", responses=AdminCreateUserSerializer)
class UsersView(APIView):
    permission_classes = (AdminPermission,)

    def get(self, request):
        users = User.objects.all()
        serializer = AdminCreateUserSerializer(users, many=True)
        return Response(serializer.data)
        
