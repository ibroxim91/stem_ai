from rest_framework import serializers
from apps.main.models import ProjectCategory, ProjectCategoryTranslation
from apps.main.models.languages import Language
from django.db.transaction import atomic

class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = ('id', 'code')


class ProjectCategoryTranslationSerializer(serializers.Serializer):
    # language = LanguageSerializer(read_only=True)
    language_id = serializers.IntegerField(required=True, source='language.id')
    language_code = serializers.CharField(read_only=True,  source='language.code')
    value = serializers.CharField(required=True, source='name')

    class Meta:
        model = ProjectCategoryTranslation
        fields = ('name',  'language')
class ProjectCategorySerializer(serializers.ModelSerializer):
    image = serializers.ImageField(required=False)
    translations = ProjectCategoryTranslationSerializer(many=True, required=False)
    parent_category = serializers.PrimaryKeyRelatedField(
        queryset=ProjectCategory.objects.all(), required=False, allow_null=True
    )

    class Meta:
        model = ProjectCategory
        fields = ('id', 'parent_category', 'image', 'translations')

    @atomic
    def create(self, validated_data):
        translations_data = validated_data.pop('translations', [])
        project_category = ProjectCategory.objects.create(**validated_data)
        for trans_data in translations_data:
            ProjectCategoryTranslation.objects.create(
                project_category=project_category,
                language_id=trans_data['language']['id'],
                name=trans_data['name']
            )
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