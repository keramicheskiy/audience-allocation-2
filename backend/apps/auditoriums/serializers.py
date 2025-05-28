from rest_framework import serializers

from apps.auditoriums.models import Auditorium
from apps.equipments.serializers import EquipmentSerializer


class AuditoriumSerializer(serializers.ModelSerializer):
    equipment = EquipmentSerializer(read_only=True)

    class Meta:
        model = Auditorium
        fields = '__all__'
