from rest_framework import serializers
from apps.main.models import ProjectCategory, ProjectCategoryTranslation, ProjectPromptTranslation
from apps.main.models.languages import Language
from django.db.transaction import atomic
from .add_language_for_data import add_languages_for_object
from rest_framework.exceptions import ValidationError

class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = ('id', 'code')

class ProjectCategoryPromptTranslationSerializer(serializers.ModelSerializer):
    language_id = serializers.IntegerField(required=True, source='language.id')
    language_code = serializers.CharField(required=False, source='language.code')
   
    class Meta:
        model = ProjectPromptTranslation
        fields = ['language_id', 'prompt', 'language_code']


class ProjectCategoryTranslationSerializer(serializers.Serializer):
    # language = LanguageSerializer(read_only=True)
    language_id = serializers.IntegerField(required=True, source='language.id')
    language_code = serializers.CharField(read_only=True,  source='language.code')
    value = serializers.CharField(required=True, source='name')

    class Meta:
        model = ProjectCategoryTranslation
        fields = ('name',  'language')
class ProjectCategorySerializer(serializers.ModelSerializer):
    image = serializers.ImageField(required=False, allow_null=True)
    translations = ProjectCategoryTranslationSerializer(many=True, required=False)
    prompts = ProjectCategoryPromptTranslationSerializer(many=True, required=True)
    parent_category = serializers.PrimaryKeyRelatedField(
        queryset=ProjectCategory.objects.all(), required=False, allow_null=True
    )

    class Meta:
        model = ProjectCategory
        fields = ('id', 'parent_category', 'image', 'translations', "prompts")

    @atomic
    def create(self, validated_data):
        translations_data = validated_data.pop('translations', [])
        prompts = validated_data.pop('prompts', [])
        project_category = ProjectCategory.objects.create(**validated_data)
        for prompt in prompts:
            language_id = prompt['language']['id']
            print()
            print("prompt ", prompt)
            print()
            if not Language.objects.filter(id=language_id).exists():
                raise ValidationError(f"Invalid language id: {language_id}")
            ProjectPromptTranslation.objects.create(
                project_category=project_category,
                language_id=language_id,
                prompt=prompt['prompt']
            )

        for trans_data in translations_data:
            exists = ProjectCategoryTranslation.objects.filter(
                project_category=project_category,
                language_id=trans_data['language']['id'],
                name=trans_data['name']
            )
            ProjectCategoryTranslation.objects.create(
                project_category=project_category,
                language_id=trans_data['language']['id'],
                name=trans_data['name']
            )
        add_languages_for_object(project_category)
        return project_category

    @atomic
    def update(self, instance, validated_data):
        translations_data = validated_data.pop('translations', [])
        instance.parent_category = validated_data.get('parent_category', instance.parent_category)
        instance.save()
        for trans_data in translations_data:
            language_id = trans_data['language']['id']
            name = trans_data['name']

            translation_obj, created = ProjectCategoryTranslation.objects.update_or_create(
                project_category=instance,
                language_id=language_id,
                defaults={'name': name}
            )

        return instance
