from rest_framework import serializers

from apps.role_approvance_requests.models import RoleForApproving


class RoleForApprovingSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoleForApproving
        fields = '__all__'
