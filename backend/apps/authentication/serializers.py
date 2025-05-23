from rest_framework import serializers

from apps.authentication.models import CustomUser


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'first_name', 'patronymic', 'last_name', 'email', 'role', 'is_verified']


class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'patronymic', 'last_name', 'email', 'password', 'role']


class LoginSerializer(serializers.Serializer):
    class Meta:
        model = CustomUser
        fields = ['email', 'password']


'''
{
"first_name": "Юрий",
"patronymic": "Иванович",
"last_name": "Битюков",
"email": "Sweetie.77@mail.ru",
"password": "qwerty",
"role": "teacher"
}
'''
