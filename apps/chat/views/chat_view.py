from rest_framework import generics, permissions
from apps.chat.models.user_chat import UserChat
from apps.chat.serializers.chat_serializer import UserChatSerializer, UserChatDetailSerializer


from drf_spectacular.utils import extend_schema


@extend_schema(tags=["Chat"], summary="User chats", request=None, responses=UserChatSerializer)
class UserChatListView(generics.ListAPIView):
    serializer_class = UserChatSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return UserChat.objects.filter(user=self.request.user)


@extend_schema(tags=["Chat"], summary="User chat detail", request=None, responses=UserChatDetailSerializer)
class UserChatDetailView(generics.RetrieveAPIView):
    serializer_class = UserChatDetailSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return UserChat.objects.filter(user=self.request.user)
    

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['user'] = self.request.user
        context['language'] = getattr(self.request.user, 'language', None)
        return context


@extend_schema(tags=["Chat"], summary="User chat delete", request=None, responses=None)
class UserChatDeleteView(generics.DestroyAPIView):
    queryset = UserChat.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return UserChat.objects.filter(user=self.request.user)