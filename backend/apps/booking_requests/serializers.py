from rest_framework import serializers

from .models import BookingRequest


class BookingRequestSerializer(serializers.ModelSerializer):
    start = serializers.DateTimeField(format="%Y-%m-%d %H:%M", input_formats=["%Y-%m-%d %H:%M"])
    end = serializers.DateTimeField(format="%Y-%m-%d %H:%M", input_formats=["%Y-%m-%d %H:%M"])

    class Meta:
        model = BookingRequest
        fields = '__all__'
