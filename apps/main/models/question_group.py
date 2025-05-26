from django.db import models
from .base import TimeStampedModel, UserStampedModel
from .project_category import ProjectCategory
from .languages import Language


class QuestionGroup( TimeStampedModel, UserStampedModel):
    category = models.ForeignKey(ProjectCategory, on_delete=models.CASCADE, related_name='question_groups')
    order = models.PositiveIntegerField(default=0)
    def __str__(self):
        default_translation = self.translations.filter(language__code='uz').first()
        if default_translation and  default_translation.name is not None:
            return default_translation.name  
        else:  
            return f'QuestionGroup {self.id}'
    class Meta:
        unique_together = ('category',  'order')    


class QuestionGroupTranslation(models.Model):
    question_group = models.ForeignKey(QuestionGroup, related_name='translations', on_delete=models.CASCADE)
    language = models.ForeignKey(Language, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, blank=True, null=True, default=None)

    class Meta:
        unique_together = ('question_group', 'language')
    
  