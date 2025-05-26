from apps.main.models.languages import Language
from apps.main.models.question import QuestionPromptTranslation, Question
from apps.main.models import ProjectCategory

def add_languages_for_object(instance,  **kwargs):
    for lang in Language.objects.all():
        if not instance.translations.filter(language=lang).exists():
            instance.translations.create(language=lang)
        if isinstance(instance, Question) :
            if not instance.prompts.filter(language=lang).exists():
                instance.prompts.create(question=instance, language=lang)    
        if  isinstance(instance, ProjectCategory):
            if not instance.prompts.filter(language=lang).exists():
                instance.prompts.create(project_category=instance, language=lang)