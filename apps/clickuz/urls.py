from .views import *
from django.urls import path

app_name = 'clickuz'


urlpatterns = [
    path('', ClickUzMerchantAPIView.as_view(), name='click'),
]    