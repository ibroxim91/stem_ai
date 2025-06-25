from django.db import models
from django.contrib.auth.models import AbstractUser
from apps.main.models import Language


class User(AbstractUser):

    class Role(models.TextChoices):
        ADMIN = 'admin', 'Admin'
        USER = 'user', 'User'

    telegram_id = models.BigIntegerField(unique=True, null=True, blank=True)
    role = models.CharField(max_length=10, choices=Role.choices, default=Role.USER)
    phone = models.CharField(max_length=14, default="")
    balance = models.IntegerField(default=0)
    language = models.ForeignKey(Language, on_delete=models.SET_NULL, blank=True, null=True)
    is_active_user = models.BooleanField(default=False)
    total_tokens = models.IntegerField(default=0)

   
    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}: {self.username}"
