from django.shortcuts import render, get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from apps.auditoriums.models import Auditorium
from apps.auditoriums.serializers import AuditoriumSerializer, AuditoriumPostSerializer
from apps.authentication import utils, tasks
from apps.authentication.decorators import role_required
from apps.lectures.models import Lecture
from apps.lectures.services import get_lecture_intervals, validate_time, validate_date


# localhost:8080/auditoriums/new
# {"number": "", "size": 1, "equipment": [1, 2], "building": 1, "description": ""}
@api_view(["GET", "POST"])
@role_required("moderator")
def create_auditorium(request):
    if request.method == "GET":
        return Response({"fields": AuditoriumPostSerializer.fields})
    elif request.method == "POST":
        serializer = AuditoriumPostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# localhost:8080/auditoriums/<auditorium_id>/change
# {"number": "", "size": 1, "equipments": [1, 2], "building": 1, "description": ""}
@api_view(["GET", "PATCH"])
@role_required("moderator")
def update_auditorium(request, auditorium_id):
    if request.method == "GET":
        return Response({"fields": AuditoriumPostSerializer.fields})
    elif request.method == "PATCH":
        auditorium = get_object_or_404(Auditorium, pk=auditorium_id)
        serializer = AuditoriumPostSerializer(auditorium, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# localhost:8080/auditoriums/<auditorium_id>/delete
@api_view(["DELETE"])
@role_required("moderator")
def delete_auditorium(request, auditorium_id):
    auditorium = get_object_or_404(Auditorium, pk=auditorium_id)
    auditorium.delete()
    return Response(status=status.HTTP_200_OK)


# localhost:8080/auditoriums/<auditorium_id>
@api_view(["GET"])
@role_required("teacher")
def get_auditorium(request, auditorium_id):
    user = utils.get_user_from_request(request)
    auditorium = get_object_or_404(Auditorium, pk=auditorium_id)

    if auditorium not in user.allowed_auditoriums.all():
        return Response({'error': 'Аудитория недоступна.'}, status=status.HTTP_403_FORBIDDEN)

    if validator := user.validate_booking_limit():
        return validator

    serializer = AuditoriumSerializer(auditorium)
    return Response({"auditorium": serializer.data}, status=status.HTTP_200_OK)


# localhost:8080/auditoriums?date=2025-12-31&start=10:45&end=12:15
@api_view(['GET'])
@role_required("teacher")
def get_auditoriums(request):
    if not request.GET.get('date', None) or not request.GET.get('start', None) or not request.GET.get('end', None):
        auditoriums = Auditorium.objects.all()
        return Response({"auditoriums": AuditoriumSerializer(auditoriums, many=True).data})
    
    if not validate_date(request.GET.get('date')):
        return Response({"error": "Дата должна быть в формате 2000-12-31."}, status=status.HTTP_400_BAD_REQUEST)
    
    if not validate_time(request.GET.get('start')) or not validate_time(request.GET.get('end')):
        return Response({"error": "Время должно быть в формате 23:59."}, status=status.HTTP_400_BAD_REQUEST)

    start, end = get_lecture_intervals(request.GET.get('date'), request.GET.get('start'), request.GET.get('end'))
    user = utils.get_user_from_request(request)
    if validator := user.validate_booking_limit():
        return validator
    if validator := user.validate_time_limit(start, end):
        return validator

    auditoriums = [a for a in user.allowed_auditoriums.all() if a.is_available(start, end)]
    return Response({'auditoriums': AuditoriumSerializer(auditoriums, many=True).data}, status=status.HTTP_200_OK)


# # localhost:8080/auditoriums/<auditorium_id>/book
# # {"date"="2025-12-31", "start"="10:45", "end"="12:15"}
# @api_view(['POST'])
# @role_required("teacher")
# def book_auditorium(request, auditorium_id):
#     start, end = get_lecture_intervals(request.data.get('date'), request.data.get('start'), request.data.get('end'))
#     auditorium = get_object_or_404(Auditorium, pk=auditorium_id)

#     if not auditorium.is_available(start, end):
#         return Response({'error': 'Аудитория уже забронироавна на указанное время.'}, status=status.HTTP_403_FORBIDDEN)

#     user = utils.get_user_from_request(request)
#     if validator := user.validate_booking_limit():
#         return validator
#     if validator := user.validate_time_limit(start, end):
#         return validator

#     Lecture.objects.create(auditorium=auditorium, date=start, end=end, user=user)
#     if user.tg_id:
#         tasks.send_telegram_message.delay(
#             f"Вы забронировали аудиторию {auditorium.id} на {request.data.get('date')} "
#             f"{request.data.get('start')}-{request.data.get('end')}", user.tg_id
#         )
#     return Response({'auditorium': AuditoriumSerializer(auditorium).data}, status=status.HTTP_200_OK)


