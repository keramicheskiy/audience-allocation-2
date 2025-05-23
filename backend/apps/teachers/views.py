from datetime import datetime

import pytz
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from apps.authentication.decorators import role_required
from apps.authentication.models import CustomUser
from apps.moderation.models import Auditorium, Equipment, Subject
from apps.moderation.serializers import AuditoriumSerializer, EquipmentSerializer, SubjectSerializer
from apps.teachers.models import Lecture
from apps.teachers.serializers import LectureSerializer
from apps.teachers.services import get_lecture_intervals
from backend.settings import tz


# Create your views here. (Lecture)


@api_view(["GET"])
@role_required("teacher")
def get_equipments(request):
    serializer = EquipmentSerializer(Equipment.objects.all(), many=True)
    return Response({"equipments": serializer.data}, status=status.HTTP_200_OK)


@api_view(["GET"])
@role_required("teacher")
def get_equipment(request, key):
    serializer = EquipmentSerializer(Equipment.objects.get(id=key))
    return Response({"equipment": serializer.data}, status=status.HTTP_200_OK)


@api_view(["GET"])
@role_required("teacher")
def get_subjects(request):
    serializer = SubjectSerializer(Subject.objects.all(), many=True)
    return Response({"subjects": serializer.data}, status=status.HTTP_200_OK)


@api_view(["GET"])
@role_required("teacher")
def get_subject(request, key):
    serializer = SubjectSerializer(Subject.objects.get(id=key))
    return Response({"subject": serializer.data}, status=status.HTTP_200_OK)


@api_view(['GET'])
@role_required('teacher')
def lectures_from_teacher(request):
    email = request.GET.get('email')
    lectures = Lecture.objects.filter(email=email).order_by('date', 'start')
    return Response({'lectures': LectureSerializer(lectures, many=True).data})


@api_view(['GET'])
@role_required('teacher')
def get_not_yet_passed_lectures(request):
    now = datetime.now(tz=tz)
    token = request.COOKIES.get('Token')
    user = Token.objects.get(key=token).user
    lectures = Lecture.objects.filter(email=user.email).order_by('date', 'start')
    not_yet_passed = []
    for lecture in lectures:
        lecture_end = lecture.get_end_datetime()
        if lecture_end > now:
            not_yet_passed.append(lecture)
    return Response({'lectures': LectureSerializer(not_yet_passed, many=True).data})


@api_view(['GET'])
@role_required("teacher")
def get_free_and_allowed_auditoriums(request):
    start, end = get_lecture_intervals(request.GET.get('date'), request.GET.get('start'), request.GET.get('end'))

    token = request.COOKIES.get('Token')
    user = Token.objects.get(key=token).user
    auditoriums = user.available_auditoriums.all()
    available = []
    for auditorium in auditoriums:
        if auditorium.is_available(start, end):
            available.append(auditorium)

    return Response({'auditoriums': AuditoriumSerializer(available, many=True).data},
                    status=status.HTTP_200_OK)


# def TODO БРОНИРОВАТЬ АУДИТОРИЮ НА УКАЗАННОЕ ВРЕМЯ
@api_view(['POST'])
@role_required("teacher")
def book_auditorium(request, auditorium_id):
    start, end = get_lecture_intervals(request.POST.get('date'), request.POST.get('start'), request.POST.get('end'))
    auditorium = get_object_or_404(Auditorium, pk=auditorium_id)
    if auditorium.is_available(start, end):
        user = Token.objects.get(key=request.COOKIES.get('Token')).user
        Lecture(auditorium=auditorium, date=start, end=end, user=user).save()
    else:
        return Response({'error': 'Auditorium is not available'}, status=status.HTTP_400_BAD_REQUEST)

# def TODO ПОЛУЧИТЬ РАЗРЕШЕННУЮ АУДИТОРИЮ


@api_view(["GET"])
@role_required("teacher")
def get_auditorium(request, key):
    serializer = AuditoriumSerializer(Auditorium.objects.get(id=key))
    return Response({"auditorium": serializer.data}, status=status.HTTP_200_OK)
