from django.shortcuts import render, get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from apps.authentication.decorators import role_required
from apps.authentication.models import CustomUser
from apps.moderation.models import Auditorium, Equipment
from apps.moderation.serializers import AuditoriumSerializer, EquipmentSerializer
from apps.teachers.models import Lecture
from apps.teachers.serializers import LectureSerializer


# Create your views here.
# Auditorium, Equipment, Subject


@api_view(['GET'])
@role_required('moderator')
def get_lectures(request):
    lectures = Lecture.objects.all().order_by('date', 'start')
    return Response({'lectures': LectureSerializer(lectures, many=True).data})


@api_view(["POST"])
@role_required("moderator")
def create_auditorium(request):
    serializer = AuditoriumSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["PUT"])
@role_required("moderator")
def update_auditorium(request, key):
    auditorium = get_object_or_404(Auditorium, pk=key)
    serializer = AuditoriumSerializer(auditorium, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["DELETE"])
@role_required("moderator")
def delete_auditorium(request, key):
    auditorium = get_object_or_404(Auditorium, pk=key)
    auditorium.delete()
    return Response(status=status.HTTP_200_OK)


@api_view(["POST"])
@role_required("moderator")
def create_equipment(request):
    serializer = EquipmentSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["PUT"])
@role_required("moderator")
def update_equipment(request, key):
    equipment = get_object_or_404(Equipment, pk=key)
    serializer = EquipmentSerializer(equipment, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["DELETE"])
@role_required("moderator")
def delete_equipment(request, key):
    equipment = get_object_or_404(Equipment, pk=key)
    equipment.delete()
    return Response(status=status.HTTP_200_OK)

# def TODO ОГРАНИЧИТЬ АУДИТОРИИ ДЛЯ ПРЕПОДА
# def TODO ОГРАНИЧИТЬ МАКСИМАЛЬНОЕ КОЛИЧЕСТВО ЧАСОВ БРОНИ ДЛЯ ПРЕПОДА
# def TODO ОГРАНИЧИТЬ КОЛИЧЕСТВО АУДИТОРИЙ ДЛЯ ПРЕПОДА
# def TODO ПОЛУЧИТЬ ВСЕ ПРЕДСТОЯЩИЕ И НЕПРОШДШИЕ ЗАНЯТИЯ (ПРЕПОДУ ТОЖЕ НУЖНА ЭТА ФУНКЦИЯ)
