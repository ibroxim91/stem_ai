from django.urls import path
from  apps.cauth.views import RegisterView, ActivateView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from apps.cauth.views.admin_crete_view import AdminUserCreateView
from apps.cauth.views.me import MeUserView
from apps.cauth.views.password_change_view import ChangePasswordView
from apps.cauth.views.password_rest_view import PasswordResetRequestView
from apps.cauth.views.set_language_view import SetLanguageView
from apps.cauth.views.users_view import UsersView
from apps.cauth.views.token_view import MyTokenObtainPairView
from apps.cauth.views.refresh_token_view import MyTokenRefreshView


urlpatterns = [
    path('me/', MeUserView.as_view(), name='me'),
    path('register/', RegisterView.as_view(), name='register'),
    path('activate/<uidb64>/<token>/', ActivateView.as_view(), name='activate'),
    path('login/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', MyTokenRefreshView.as_view(), name='token_refresh'),
    path('admin/create/', AdminUserCreateView.as_view(), name='admin-user-create'),
    path('set-language/', SetLanguageView.as_view(), name='admin-user-create'),
    path('users/', UsersView.as_view(), name='users'),
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
     path('password-reset/', PasswordResetRequestView.as_view(), name='password-reset'),
]
