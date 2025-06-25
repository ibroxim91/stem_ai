# models.py
from django.db import models
from apps.main.models.languages import Language

class BotTranslation(models.Model):
    language = models.ForeignKey(Language, on_delete=models.CASCADE)
    translations = models.JSONField() 


    def __str__(self):
        return self.language.name
