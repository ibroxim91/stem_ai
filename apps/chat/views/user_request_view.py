from rest_framework.views import APIView
from apps.chat.models.user_chat import UserChat
from apps.chat.serializers.user_request_serializer import UserRequestSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from apps.chat.services.user_request_service import UserRequestService


class UserRequestView(APIView):
    serializer_class = UserRequestSerializer
    permission_classes = [IsAuthenticated]
    def post(self, request):
        serializer = UserRequestSerializer(data=request.data)
        chat = None
        if serializer.is_valid():
            if serializer.validated_data.get('chat_id'):
                chat_id = serializer.validated_data.get('chat_id')
                chat = UserRequestService.get_object(chat_id, UserChat, "Chat")
            result = UserRequestService.build_response(request.user, serializer.validated_data, chat)
            if result:
                return Response(result, status=status.HTTP_200_OK)
            else:
                data = {"result": "Something went wrong"}
                return Response(data, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)