from django.urls import path, include
from apps.chat.views.user_request_view import UserRequestView
from django.urls import path
from apps.chat.views.chat_view import UserChatListView, UserChatDetailView
from rest_framework.routers import DefaultRouter
from apps.chat.views.tarif_view import TariffViewSet

router = DefaultRouter()
router.register(r'tariffs', TariffViewSet, basename='tariff')

urlpatterns = [
    path('request/', UserRequestView.as_view(), name='user-request'),
    path('', UserChatListView.as_view(), name='userchat-list'),
    path('<int:pk>/', UserChatDetailView.as_view(), name='userchat-detail'),
    path('', include(router.urls)),
]


