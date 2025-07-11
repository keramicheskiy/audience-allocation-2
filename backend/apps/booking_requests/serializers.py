from rest_framework import serializers

from .models import BookingRequest
from apps.authentication.serializers import CustomUserSerializer
from apps.authentication.models import CustomUser
from apps.auditoriums.models import Auditorium
from apps.auditoriums.serializers import AuditoriumSerializer


class BookingRequestPostSerializer(serializers.ModelSerializer):
    start = serializers.DateTimeField(format="%Y-%m-%d %H:%M", input_formats=["%Y-%m-%d %H:%M"])
    end = serializers.DateTimeField(format="%Y-%m-%d %H:%M", input_formats=["%Y-%m-%d %H:%M"])
    user = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all(), allow_null=True)
    auditorium = serializers.PrimaryKeyRelatedField(queryset=Auditorium.objects.all(), allow_null=True)

    class Meta:
        model = BookingRequest
        fields = '__all__'

    


class BookingRequestSerializer(serializers.ModelSerializer):
    start = serializers.DateTimeField(format="%Y-%m-%d %H:%M", input_formats=["%Y-%m-%d %H:%M"])
    end = serializers.DateTimeField(format="%Y-%m-%d %H:%M", input_formats=["%Y-%m-%d %H:%M"])
    user = CustomUserSerializer(read_only=True)
    auditorium = AuditoriumSerializer(read_only=True)

    class Meta:
        model = BookingRequest
        fields = '__all__'
