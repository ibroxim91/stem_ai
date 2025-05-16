from django.db import models

class Language(models.Model):
    code = models.CharField(max_length=10, unique=True, help_text='uz, ru, en')  # 'uz', 'ru', 'en'
    name = models.CharField(max_length=100, help_text='O\'zbekcha, Русский, English')  # O'zbekcha, Русский, English

    def __str__(self):
        return self.name
