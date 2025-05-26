# apps/payments/serializers.py
from rest_framework import serializers
from apps.cauth.models import Tariff, TariffTranslation
from apps.main.models.languages import Language
from django.db import transaction
from apps.main.serializers.add_language_for_data import add_languages_for_object


class TariffTranslationSerializer(serializers.ModelSerializer):
    language_id = serializers.IntegerField(write_only=True)
    language_code = serializers.CharField(read_only=True, source='language.code')

    class Meta:
        model = TariffTranslation
        fields = ('id', 'language_id', 'language_code', 'name', 'description')

class TariffSerializer(serializers.ModelSerializer):
    translations = TariffTranslationSerializer(many=True)

    class Meta:
        model = Tariff
        fields = ('id', 'price', 'tokens', 'translations')

    @transaction.atomic
    def create(self, validated_data):
        translations_data = validated_data.pop('translations', [])
        if Tariff.objects.filter(price=validated_data['price'], tokens=validated_data['tokens']).exists(): 
            raise serializers.ValidationError("Tariff already exists")
        tariff = Tariff.objects.create(**validated_data)
        for td in translations_data:
            lang_id = td.pop('language_id')
            Language.objects.get(id=lang_id)  # ValidationError bo'lsa chiqadi
            TariffTranslation.objects.create(
                tarif=tariff,
                language_id=lang_id,
                **td
            )
        add_languages_for_object(tariff)    
        return tariff

    @transaction.atomic
    def update(self, instance, validated_data):
        translations_data = validated_data.pop('translations', [])
        instance.price  = validated_data.get('price', instance.price)
        instance.tokens = validated_data.get('tokens', instance.tokens)
        instance.save()

        # nested translations update/create
        for td in translations_data:
            lang_id = td.pop('language_id')
            TariffTranslation.objects.update_or_create(
                tarif=instance,
                language_id=lang_id,
                defaults={
                    'name': td.get('name'),
                    'description': td.get('description', '')
                }
            )
        return instance
