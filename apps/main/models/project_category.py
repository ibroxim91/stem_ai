from django.db import models
from .base import TimeStampedModel, UserStampedModel
from .languages import Language


class ProjectCategory( TimeStampedModel, UserStampedModel):
    parent_category = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL)
    image = models.ImageField(upload_to='project_category/', null=True, blank=True)
    def __str__(self):
        default_translation = self.translations.filter(language__code='uz').first()
        return default_translation.name if default_translation else 'No name'


class ProjectCategoryTranslation(models.Model):
    project_category = models.ForeignKey(ProjectCategory, related_name='translations', on_delete=models.CASCADE)
    language = models.ForeignKey(Language, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, blank=True, null=True, default=None)

    class Meta:
        unique_together = ('project_category', 'language')
        