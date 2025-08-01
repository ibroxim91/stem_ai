from django.db import models
from .languages import Language
from apps.main.models.base import TimeStampedModel, UserStampedModel
from .question_group import QuestionGroup


class Question( TimeStampedModel, UserStampedModel):
    TYPE_CHOICES = (
        ('boolean', 'Boolean'),
        ('select', 'Select'),
    )

    group = models.ForeignKey(QuestionGroup, on_delete=models.CASCADE, related_name='questions')
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)

    def __str__(self):
        default_translation = self.translations.filter(language__code='uz').first()
        if default_translation and  default_translation.name is not None:
            return default_translation.name  
        else:  
            return f'{self.__class__.__name__} {self.id}' 


class QuestionPromptTranslation(models.Model):
    question = models.ForeignKey(Question, related_name='prompts', on_delete=models.CASCADE)
    language = models.ForeignKey(Language, on_delete=models.CASCADE)
    prompt = models.CharField(max_length=255, blank=True, null=True, default=None)
    
    class Meta:
        unique_together = ('question', 'language')

 
class QuestionTranslation(models.Model):
    question = models.ForeignKey(Question, related_name='translations', on_delete=models.CASCADE)
    language = models.ForeignKey(Language, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, blank=True, null=True, default=None)
    
    class Meta:
        unique_together = ('question', 'language')

        
class QuestionOption(TimeStampedModel, UserStampedModel):
    question = models.ForeignKey(
        'Question',
        on_delete=models.CASCADE,
        related_name='options'
    )


    def __str__(self):
        default_translation = self.translations.filter(language__code='uz').first()
        if default_translation and  default_translation.value is not None:
            return default_translation.value  
        else:  
            return f'{self.__class__.__name__} {self.id}' 
 


class QuestionOptionTranslation(models.Model):
    question_option = models.ForeignKey(QuestionOption, related_name='translations', on_delete=models.CASCADE)
    language = models.ForeignKey(Language, on_delete=models.CASCADE)
    value = models.CharField(max_length=255, blank=True, null=True, default=None) 
    
    
    class Meta:
        unique_together = ('question_option', 'language')

  