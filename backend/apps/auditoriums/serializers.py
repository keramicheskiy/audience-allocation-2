from rest_framework import serializers

from apps.auditoriums.models import Auditorium
from apps.equipments.serializers import EquipmentSerializer
from apps.equipments.models import Equipment
from apps.buildings.serializers import BuildingSerializer
from apps.buildings.models import Building


class AuditoriumPostSerializer(serializers.ModelSerializer):
    equipments = serializers.PrimaryKeyRelatedField(
        queryset=Equipment.objects.all(),
        many=True  # Так как это ManyToManyField, если забыл, иди загугли, я тебе не буду опять объяснять, маленький толстый мальчик
    )
    building = serializers.PrimaryKeyRelatedField(queryset=Building.objects.all(), allow_null=True)

    class Meta:
        model = Auditorium
        fields = '__all__'

    def create(self, validated_data):
        # Извлекаем equipment, так как ManyToMany нельзя сохранить напрямую через create()
        equipments = validated_data.pop('equipments', [])
        auditorium = Auditorium.objects.create(**validated_data)
        auditorium.equipments.set(equipments)  # Устанавливаем связь ManyToMany
        return auditorium

    def update(self, instance, validated_data):
        equipments = validated_data.pop('equipments', None)
        if equipments is not None:
            instance.equipments.set(equipments)
        return super().update(instance, validated_data)
    

class AuditoriumSerializer(serializers.ModelSerializer):
    equipments = EquipmentSerializer(many=True, read_only=True)
    building = BuildingSerializer(read_only=True)

    class Meta:
        model = Auditorium
        fields = '__all__'