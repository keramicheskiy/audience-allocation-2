from rest_framework import serializers

from apps.authentication.serializers import CustomUserSerializer
from apps.role_approvance_requests.models import RoleForApproving


class RoleForApprovingSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer(read_only=True)

    class Meta:
        model = RoleForApproving
        fields = '__all__'
