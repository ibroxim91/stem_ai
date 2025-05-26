from .views import *
from apps.order.views.order_view import OrderCreateView
from django.urls import path

app_name = 'order'


urlpatterns = [
    path('',OrderCreateView.as_view(), name="order_create" ),      
    # path('payme', PaymentView.as_view(), name='payme'),
    # path('click',ClickApiView.as_view(), name='click'),
]    