from rest_framework import serializers

from apps.administration.models import RoleForApproving


class RoleForApprovingSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoleForApproving
        fields = '__all__'


