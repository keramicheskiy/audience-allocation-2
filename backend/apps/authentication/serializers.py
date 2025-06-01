from rest_framework import serializers

from apps.auditoriums.serializers import AuditoriumSerializer
from apps.authentication.models import CustomUser


class CustomUserSerializer(serializers.ModelSerializer):
    allowed_auditoriums = AuditoriumSerializer(read_only=True, many=True)

    class Meta:
        model = CustomUser
        fields = [
            'id', 'first_name', 'patronymic', 'last_name', 'email', 'role',
            'is_verified', 'booking_limit', 'hours_limit', 'allowed_auditoriums', 'tg_id'
        ]


class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'patronymic', 'last_name', 'email', 'password', 'role', 'tg_id']


class LoginSerializer(serializers.Serializer):
    class Meta:
        model = CustomUser
        fields = ['email', 'password', 'tg_id']
