from django.urls import path
from  apps.cauth.views import RegisterView, ActivateView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from apps.cauth.views.admin_crete_view import AdminUserCreateView
from apps.cauth.views.set_language_view import SetLanguageView


urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('activate/<uidb64>/<token>/', ActivateView.as_view(), name='activate'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('admin/create/', AdminUserCreateView.as_view(), name='admin-user-create'),
    path('set-language/', SetLanguageView.as_view(), name='admin-user-create'),
]
