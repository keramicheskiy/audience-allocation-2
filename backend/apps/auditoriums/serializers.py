from rest_framework import serializers

from apps.auditoriums.models import Auditorium


class AuditoriumSerializer(serializers.ModelSerializer):
    class Meta:
        model = Auditorium
        fields = '__all__'
