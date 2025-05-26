from django.db import models
from apps.order.models import Order

class PaycomTransaction(models.Model):
    paycom_transaction_id = models.CharField(max_length=255, null=False, unique=True)
    paycom_time = models.CharField(max_length=15)
    paycom_time_datetime = models.DateTimeField(null=False)
    create_time = models.DateTimeField(auto_now_add=True)
    perform_time = models.DateTimeField(null=True, blank=True)
    cancel_time = models.DateTimeField(null=True, blank=True)
    amount = models.CharField(max_length=50, null=False)
    state = models.IntegerField(null=False)
    reason = models.IntegerField(null=True, blank=True)
    receivers = models.TextField(null=True, blank=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.paycom_transaction_id
