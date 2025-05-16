from django.db import models
from .user import User
from .tariff import Tariff


class UserTariffHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tariff_history')
    tariff = models.ForeignKey(Tariff, on_delete=models.SET_NULL, null=True)
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField()
    amount_paid = models.PositiveIntegerField(default=0)
    is_paid = models.BooleanField(default=False)  # To'lov qilinganmi yoki yo'q
    is_active = models.BooleanField(default=True)  # Hozirgi faol tarifmi

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.tariff.name} ({self.start_date.date()} - {self.end_date.date()})"