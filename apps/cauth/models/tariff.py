from django.db import models

from apps.main.models.languages import Language



class Tariff(models.Model):
    price = models.DecimalField(max_digits=10, decimal_places=2)
    tokens = models.IntegerField()
    
    def __str__(self):
        return str(self.price)
    

class TariffTranslation(models.Model):
    tarif = models.ForeignKey(Tariff, related_name='translations', on_delete=models.CASCADE)
    language = models.ForeignKey(Language, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, blank=True, null=True, default=None)
    description = models.TextField(blank=True)

    class Meta:
        unique_together = ('tarif', 'language')
    