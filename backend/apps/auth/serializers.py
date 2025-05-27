from rest_framework import serializers

from apps.auth.models import CustomUser


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'first_name', 'patronymic', 'last_name', 'email', 'role', 'is_verified', 'booking_limit',
                  'hours_limit']


class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'patronymic', 'last_name', 'email', 'password', 'role']


class LoginSerializer(serializers.Serializer):
    class Meta:
        model = CustomUser
        fields = ['email', 'password']
