from rest_framework import serializers
from apps.main.models import QuestionGroup, QuestionGroupTranslation
from django.db.transaction import atomic
from rest_framework.exceptions import ValidationError
from apps.main.models.languages import Language
from apps.main.models.project_category import ProjectCategory



class QuestionGroupTranslationSerializer(serializers.Serializer):
    language_id = serializers.IntegerField(required=True, source='language.id')
    language_code = serializers.CharField(read_only=True,  source='language.code')
    value = serializers.CharField(required=True, source='name')

    class Meta:
        model = QuestionGroupTranslation
        fields = ('name',  'language')
class QuestionGroupSerializer(serializers.ModelSerializer):
    project = serializers.IntegerField(required=True, source='category.id')
    translations = QuestionGroupTranslationSerializer(many=True, required=False)
    

    class Meta:
        model = QuestionGroup
        fields = ('id', 'project',  'translations')

    @atomic
    def create(self, validated_data):
        translations_data = validated_data.pop('translations', [])
        project_id = validated_data.pop('category')['id']
        category = ProjectCategory.objects.get(id=int(project_id))
        question_group = QuestionGroup.objects.create(category=category, **validated_data )
        print("Filter ", QuestionGroupTranslation.objects.filter(question_group=question_group))
        for trans_data in translations_data:
            language_id = trans_data['language']['id']
            if not Language.objects.filter(id=language_id).exists():
                raise ValidationError(f"Invalid language id: {language_id}")
            QuestionGroupTranslation.objects.get_or_create(
                question_group=question_group,
                language_id=language_id,
                name=trans_data['name']
            )
        return question_group

    @atomic
    def update(self, instance, validated_data):
        translations_data = validated_data.pop('translations', [])
        instance.category = validated_data.get('project', instance.category)
        instance.save()
        for trans_data in translations_data:
            language_id = trans_data['language']['id']
            name = trans_data['name']
            if not Language.objects.filter(id=language_id).exists():
                raise ValidationError(f"Invalid language id: {language_id}")    
            translation_obj, created = QuestionGroupTranslation.objects.update_or_create(
                question_group=instance,
                language_id=language_id,
                defaults={'name': name}
            )

        return instance