from apps.main.models.languages import Language
from apps.main.models.project_category import ProjectCategory
from apps.main.models.question_group import QuestionGroup
from apps.main.models.question import Question, QuestionOption

from django.dispatch import receiver
from django.db.models.signals import post_save


@receiver(post_save, sender=Language)
def add_language(sender, instance, created, **kwargs):
    if created:
        for p_category in ProjectCategory.objects.all():
            p_category.translations.create(language=instance)
        for q_category in QuestionGroup.objects.all():
            q_category.translations.create(language=instance)
        for question in Question.objects.all():
            question.translations.create(language=instance)   
            question.prompts.create(language=instance)   
        for option in QuestionOption.objects.all():
            option.translations.create(language=instance)     

