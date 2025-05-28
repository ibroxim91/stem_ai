# serializers.py

from rest_framework import serializers
from apps.cauth.models import User

class AdminCreateUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)
    email_verified = serializers.BooleanField(read_only=True, source='is_active')

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'phone', 'role', 'email_verified', 'password' , 'email', 'is_active_user', 'total_tokens']

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.role = 'admin'
        user.save()
        return user
