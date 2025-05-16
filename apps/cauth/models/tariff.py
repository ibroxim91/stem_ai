from django.db import models


class Tariff(models.Model):
    name = models.CharField(max_length=100)  # Gold, Silver, Free va h.k.
    daily_limit = models.PositiveIntegerField(default=20)
    price = models.PositiveIntegerField(default=0)
    active_days = models.PositiveIntegerField(default=30)


    def __str__(self):
        return self.name