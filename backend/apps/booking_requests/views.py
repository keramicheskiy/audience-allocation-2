from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import BookingRequest
from .serializers import BookingRequestSerializer
from apps.authentication.decorators import role_required

from datetime import datetime
from .services import notify_request_expired, notify_booking_request_accepted, notify_booking_request_declined
from apps.lectures.models import Lecture
from apps.authentication import utils
from django.shortcuts import get_object_or_404
from backend.settings import time_zone


# localhost:8080/booking/requests
@api_view(["GET"])
@role_required('moderator')
def get_booking_requests(request):
    reqs = BookingRequest.objects.all()
    for req in reqs:
        if req.end < datetime.now():
            reqs.remove(req)
            notify_request_expired(req)
            req.delete()
    serializer = BookingRequestSerializer(reqs, many=True)
    return Response({"requests": serializer.data})


# localhost:8080/booking/requests/add
# {auditorium: 1, "start"="2025-12-31 10:45", "end"="2025-12-31 12:15"}
@api_view(["POST"])
@role_required('teacher')
def add_booking_request(request):
    request.data["user"] = utils.get_user_from_request(request).id

    serializer = BookingRequestSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    user = serializer.validated_data.get('user')
    auditorium = serializer.validated_data.get('auditorium')
    start_time = serializer.validated_data.get('start')
    end_time = serializer.validated_data.get('end')

    if end_time < datetime.now(tz=time_zone):
        return Response({"errors": "Нельзя забронировать аудиторию на прошедшую дату."}, status.HTTP_403_FORBIDDEN)

    if Lecture.objects.filter(auditorium=auditorium, end__gt=start_time, start__lt=end_time).exists():
        return Response({"error": "Аудитория уже занята на это время."}, status=status.HTTP_409_CONFLICT)
    
    if not user.allowed_auditoriums.filter(id=auditorium.id).exists():
        return Response({"error": "Данная аудитория недоступна для вашего аккаунта."}, status=status.HTTP_403_FORBIDDEN)
    
    if not(user.validate_booking_limit()):  # Checking if a user has ability to book one more lecture
        return Response({"errors": "У вас уже забронировано максимальное количество лекций."}, status=status.HTTP_403_FORBIDDEN)
    
    if not(user.validate_time_limit(start_time, end_time)):  # Checking if a user can book this much hours
        return Response({"errors": "Количество часов, запрошенное вами на бронь, превышает лимит."}, status=status.HTTP_403_FORBIDDEN)
    
    serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)


# localhost:8080/booking/requests/<request_id>
# {}
@api_view(["POST", "DELETE"])
@role_required('moderator')
def manage_booking_request(request, request_id):
    if request.method == "POST":
        req = get_object_or_404(BookingRequest, pk=request_id)

        if req.end < datetime.now(tz=time_zone):
            req.delete()
            notify_request_expired(req)
            return Response({"errors": "Нельзя забронировать аудиторию на прошедшую дату."}, status.HTTP_403_FORBIDDEN)

        if Lecture.objects.filter(auditorium=req.auditorium, end__gt=req.start, start__lt=req.end).exists():
            return Response({"error": "Аудитория уже занята на это время."}, status=status.HTTP_409_CONFLICT)
        
        if not req.user.allowed_auditoriums.filter(id=req.auditorium.id).exists():
            return Response({"error": "Данная аудитория более не доступна для этого пользователя."}, status=status.HTTP_403_FORBIDDEN)
    
        if not(req.user.validate_booking_limit()):
            return Response({"errors": "У пользователя уже забронировано максимальное количество лекций."}, status=status.HTTP_403_FORBIDDEN)
        
        if not(req.user.validate_time_limit(req.start, req.end)):
            return Response({"errors": "Количество часов превышает лимит."}, status=status.HTTP_403_FORBIDDEN)

        Lecture.objects.create(user=req.user, auditorium=req.auditorium, start=req.start, end=req.end).save()
        req.delete()
        notify_booking_request_accepted(req)

        return Response(status=status.HTTP_200_OK)
    
    elif request.method == "DELETE":
        req = get_object_or_404(BookingRequest, pk=request_id)
        req.delete()
        notify_booking_request_declined(req)

        return Response(status=status.HTTP_204_NO_CONTENT)

