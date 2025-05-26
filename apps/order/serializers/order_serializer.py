from django.db import transaction
from rest_framework import serializers
from apps.order.models.order import Order




class OrderSerializer(serializers.ModelSerializer):
    total_price = serializers.ReadOnlyField()
    status = serializers.ReadOnlyField()
    payment_status = serializers.ReadOnlyField()
    user = serializers.ReadOnlyField()
    payment_type = serializers.CharField(required=True, max_length=20)
    

    class Meta:
        model = Order
        fields = ["id", "user", "total_price", "tariff", "payment_type", "status", "payment_status"]

