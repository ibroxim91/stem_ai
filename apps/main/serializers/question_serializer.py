from rest_framework import serializers
from apps.main.models import (
    Question, QuestionTranslation, QuestionOption, QuestionOptionTranslation, QuestionPromptTranslation
)
from apps.main.models.languages import Language
from apps.main.models.question_group import QuestionGroup
from django.db.transaction import atomic
from rest_framework.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from .add_language_for_data import add_languages_for_object


class QuestionOptionTranslationSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    language_id = serializers.IntegerField(required=True)
    language_code = serializers.CharField(required=False)
   
    
    class Meta:
        model = QuestionOptionTranslation
        fields = ['id', 'language_id', 'value', 'language_code']


class QuestionOptionSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    translations = QuestionOptionTranslationSerializer(many=True)

    class Meta:
        model = QuestionOption
        fields = ['id', 'translations']


class QuestionTranslationSerializer(serializers.ModelSerializer):
    language_id = serializers.IntegerField(required=True, source='language.id')
    language_code = serializers.CharField(required=False, source='language.code')
    value = serializers.CharField(required=True, source='name')
   
    class Meta:
        model = QuestionTranslation
        fields = ['language_id', 'value', 'language_code']


class QuestionPromptTranslationSerializer(serializers.ModelSerializer):
    language_id = serializers.IntegerField(required=True, source='language.id')
    language_code = serializers.CharField(required=False, source='language.code')
   
    class Meta:
        model = QuestionPromptTranslation
        fields = ['language_id', 'prompt', 'language_code']


class QuestionSerializer(serializers.ModelSerializer):
    translations = QuestionTranslationSerializer(many=True, required=True)
    prompts = QuestionPromptTranslationSerializer(many=True, write_only=True, required=True)
    options = QuestionOptionSerializer(many=True, required=False)
    group = serializers.PrimaryKeyRelatedField(queryset=QuestionGroup.objects.all())

    class Meta:
        model = Question
        fields = [
            'id', 'group', 'type', 'prompts',
            'translations', 'options'
        ]
    @atomic
    def create(self, validated_data):
        translations_data = validated_data.pop('translations')
        options_data = validated_data.pop('options', [])
        prompts = validated_data.pop('prompts', [])
        group = validated_data.pop('group')
        if not translations_data:
            raise ValidationError("Translations data is required.")

        # Create main question
        question = Question.objects.create(group=group, **validated_data)

        for prompt in prompts:
            language_id = prompt['language']['id']
            if not Language.objects.filter(id=language_id).exists():
                raise ValidationError(f"Invalid language id: {language_id}")
            QuestionPromptTranslation.objects.create(
                question=question,
                language_id=language_id,
                prompt=prompt['prompt']
            )

        # Create translations
        for translation_data in translations_data:
            language_id = translation_data['language']['id']
            if not Language.objects.filter(id=language_id).exists():
                raise ValidationError(f"Invalid language id: {language_id}")
            QuestionTranslation.objects.create(
                question=question,
                language_id=language_id,
                name=translation_data['name']
            )

        # Create options and their translations
        for option_data in options_data:
            option_translations = option_data.pop('translations', [])
            option = QuestionOption.objects.create(question=question)
            for translation_data in option_translations:
                language_id = translation_data['language_id']
                if not Language.objects.filter(id=language_id).exists():
                    raise ValidationError(f"Invalid language id: {language_id}")
                QuestionOptionTranslation.objects.create(
                    question_option=option,
                    language_id=language_id,
                    value=translation_data['value']
                )
            add_languages_for_object(option)
        add_languages_for_object(question)
        return question

    @atomic
    def update(self, instance, validated_data):
        translations_data = validated_data.pop('translations', [])
        options_data = validated_data.pop('options', [])
        group = validated_data.get('group', instance.group)

        # Yangilash: asosiy maydonlar
        instance.type = validated_data.get('type', instance.type)
        instance.prompt = validated_data.get('prompt', instance.prompt)
        instance.group = group
        instance.save()

        for translation_data in translations_data:
            language_id = translation_data['language']['id']
            if not Language.objects.filter(id=language_id).exists():
                raise ValidationError(f"Invalid language id: {language_id}")
            QuestionTranslation.objects.update_or_create(
                question=instance,
                language_id=language_id,
               defaults={'name': translation_data['name']}
            )

        if  instance.type == 'select' and  options_data:    
            for option_data in options_data:
                option_translations = option_data.pop('translations', [])
                if option_data.get('id'):
                    option =  get_object_or_404(QuestionOption, id=option_data['id'])
                else:
                    option = QuestionOption.objects.create(question=instance)
                for translation_data in option_translations:
                    language_id = translation_data['language_id']
                    if not Language.objects.filter(id=language_id).exists():
                        raise ValidationError(f"Invalid language id: {language_id}")
                    QuestionOptionTranslation.objects.update_or_create(
                        question_option=option,
                        language_id=language_id,
                        defaults={'value': translation_data['value']}
                    )
        else:
            raise ValidationError("Options data is required for 'select' type questions.")
        return instance


