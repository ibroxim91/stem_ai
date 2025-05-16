from apps.main.models.languages import Language


def add_languages_for_object(instance,  **kwargs):
    for lang in Language.objects.all():
        if not instance.translations.filter(language=lang).exists():
            instance.translations.create(language=lang)
