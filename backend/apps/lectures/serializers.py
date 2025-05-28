from rest_framework import serializers

from apps.auditoriums.serializers import AuditoriumSerializer
from apps.authentication.serializers import CustomUserSerializer
from apps.lectures.models import Lecture


class LectureSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer(read_only=True)
    auditorium = AuditoriumSerializer(read_only=True)

    class Meta:
        model = Lecture
        fields = '__all__'
