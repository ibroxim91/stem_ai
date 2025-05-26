from django.db import models
from apps.cauth.models.tariff import Tariff
from apps.cauth.models.user import User



# ORDER

class OrderStatus(models.IntegerChoices):
    created = 1, "created"  # Buyurtma ochildi
    on_process = 2, "on process"  # Buyurtma jarayonida
    verified = 3, "verified"  # Buyurtma tasdiqlandi
    delivered = 4, "delivered"  # Buyurtma to'landi
    cancelled = 0, "cancelled "  # Bekor qilindi


class PaymentType(models.TextChoices):
    click = "click", "Click"
    payme = "payme", "Payme"
    stripe = "stripe", "Stripe"

class PaymentStatus(models.IntegerChoices):
    unpaid = 0, "To'lanmadi"
    paid = 1, "To'landi"

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Buyurtma qiluvchi")
    total_price = models.PositiveIntegerField("Narxi", default=0)
    tariff = models.ForeignKey(Tariff, on_delete=models.CASCADE, related_name="order", verbose_name="Tarif")
    payment_type = models.CharField( "Status", choices=PaymentType.choices, default=PaymentType.click.value)
    status = models.SmallIntegerField( "Status", choices=OrderStatus.choices, default=OrderStatus.created.value)
    payment_status = models.SmallIntegerField("To'lov holati", choices=PaymentStatus.choices, default=0)

    class Meta:
        verbose_name = "Buyurtma"
        verbose_name_plural = "Buyurtmalar"

    def __str__(self):
        return str(self.pk)

