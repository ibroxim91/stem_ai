from apps.cauth.models import User
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from rest_framework.validators import UniqueValidator

from apps.main.models.languages import Language

class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    language = serializers.PrimaryKeyRelatedField(queryset=Language.objects.all(), help_text='Language ID')
    # password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'language']

    # def validate(self, attrs):
    #     if attrs['password'] != attrs['password2']:
    #         raise serializers.ValidationError({"password": "Passwords do not match"})
    #     return attrs

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            language=validated_data['language'],
            email=validated_data['email'],
            password=validated_data['password'],
            is_active=False  # Faollashtirish linkidan keyin aktiv bo'ladi
        )
        return user
