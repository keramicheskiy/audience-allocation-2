from datetime import datetime

import pytz
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from apps.authentication import utils
from apps.authentication.decorators import role_required
from apps.authentication.models import CustomUser
from apps.authentication.serializers import CustomUserSerializer
from apps.moderation.models import Auditorium, Equipment
from apps.moderation.serializers import AuditoriumSerializer, EquipmentSerializer
from apps.teachers.models import Lecture
from apps.teachers.serializers import LectureSerializer
from apps.teachers.services import get_lecture_intervals


# localhost:8080/teachers/equipments
@api_view(["GET"])
@role_required("teacher")
def get_equipments(request):
    serializer = EquipmentSerializer(Equipment.objects.all(), many=True)
    return Response({"equipments": serializer.data}, status=status.HTTP_200_OK)


# localhost:8080/teachers/my/lectures
@api_view(["GET"])
@role_required("teacher")
def get_own_lectures(request):
    user = utils.get_user_from_request(request)
    lectures = Lecture.objects.filter(email=user.email).order_by('date', 'start').all()
    return Response({"lectures": LectureSerializer(lectures, many=True).data}, status=status.HTTP_200_OK)


# localhost:8080/teachers/my/lectures/upcoming
@api_view(['GET'])
@role_required('teacher')
def get_upcoming_lectures(request):
    user = utils.get_user_from_request(request)
    upcoming_lectures = user.get_upcoming_lectures()
    return Response({'lectures': LectureSerializer(upcoming_lectures, many=True).data})


# localhost:8080/teachers/auditoriums?date=2025-12-31&start=10:45&end=12:15
@api_view(['GET'])
@role_required("teacher")
def get_free_auditoriums(request):
    start, end = get_lecture_intervals(request.GET.get('date'), request.GET.get('start'), request.GET.get('end'))

    user = utils.get_user_from_request(request)
    if validator := user.validate_booking_limit():
        return validator
    if validator := user.validate_time_limit(start, end):
        return validator

    auditoriums = [a for a in user.allowed_auditoriums.all() if a.is_available(start, end)]
    return Response({'auditoriums': AuditoriumSerializer(auditoriums, many=True).data}, status=status.HTTP_200_OK)


# localhost:8080/teachers/auditoriums/<auditorium_id>/book
# {"date"="2025-12-31", "start"="10:45", "end"="12:15"}
@api_view(['POST'])
@role_required("teacher")
def book_auditorium(request, auditorium_id):
    start, end = get_lecture_intervals(request.POST.get('date'), request.POST.get('start'), request.POST.get('end'))
    auditorium = get_object_or_404(Auditorium, pk=auditorium_id)

    if not auditorium.is_available(start, end):
        return Response({'error': 'Аудитория уже забронироавна на указанное время.'}, status=status.HTTP_403_FORBIDDEN)

    user = utils.get_user_from_request(request)
    if validator := user.validate_booking_limit():
        return validator
    if validator := user.validate_time_limit(start, end):
        return validator

    Lecture.objects.create(auditorium=auditorium, date=start, end=end, user=user)
    return Response({'auditorium': AuditoriumSerializer(auditorium).data}, status=status.HTTP_200_OK)


# localhost:8080/teachers/auditoriums/<auditorium_id>
@api_view(["GET"])
@role_required("teacher")
def get_auditorium(request, key):
    user = utils.get_user_from_request(request)
    auditorium = get_object_or_404(Auditorium, pk=key)

    if auditorium not in user.allowed_auditoriums.all():
        return Response({'error': 'Аудитория недоступна.'}, status=status.HTTP_403_FORBIDDEN)

    if validator := user.validate_booking_limit():
        return validator

    serializer = AuditoriumSerializer(auditorium)
    return Response({"auditorium": serializer.data}, status=status.HTTP_200_OK)


# localhost:8080/administration/users/{user_id}
@api_view(["GET"])
@role_required("teacher")
def get_user(request, user_id):
    user = get_object_or_404(CustomUser, pk=user_id)
    return Response({"user": CustomUserSerializer(user).data}, status=status.HTTP_200_OK)
