from django.shortcuts import render, get_object_or_404
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view
from rest_framework.response import Response

from apps.authentication import utils
from apps.authentication.decorators import role_required
from apps.authentication.models import CustomUser
from apps.moderation.models import Auditorium, Equipment
from apps.moderation.serializers import AuditoriumSerializer, EquipmentSerializer
from apps.teachers.models import Lecture
from apps.teachers.serializers import LectureSerializer


# localhost:8080/moderation/lectures
@api_view(['GET'])
@role_required('moderator')
def get_lectures(request):
    lectures = Lecture.objects.all().order_by('date', 'start')
    return Response({'lectures': LectureSerializer(lectures, many=True).data})


# localhost:8080/moderation/auditoriums/new
# {"number": "", "size": 1, "equipment": 1, "location": "", "description": ""}
@api_view(["POST"])
@role_required("moderator")
def create_auditorium(request):
    serializer = AuditoriumSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# localhost:8080/moderation/auditoriums/<auditorium_id>
# {"number": "", "size": 1, "equipment": 1, "location": "", "description": ""}
@api_view(["PATCH", "DELETE"])
@role_required("moderator")
def manage_auditorium(request, auditorium_id):
    if request.method == "PATCH":
        auditorium = get_object_or_404(Auditorium, pk=auditorium_id)
        serializer = AuditoriumSerializer(auditorium, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == "DELETE":
        auditorium = get_object_or_404(Auditorium, pk=auditorium_id)
        auditorium.delete()
        return Response(status=status.HTTP_200_OK)


# localhost:8080/moderation/equipments/new
# {"name": ""}
@api_view(["POST"])
@role_required("moderator")
def create_equipment(request):
    serializer = EquipmentSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# localhost:8080/moderation/equipments/<equipment_id>
# {"name": ""}
@api_view(["PATCH", "DELETE"])
@role_required("moderator")
def manage_equipment(request, equipment_id):
    if request.method == "PATCH":
        equipment = get_object_or_404(Equipment, pk=equipment_id)
        serializer = EquipmentSerializer(equipment, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == "DELETE":
        equipment = get_object_or_404(Equipment, pk=equipment_id)
        equipment.delete()
        return Response(status=status.HTTP_200_OK)


# localhost:8080/moderation/users/<user_id>/lectures
@api_view(["GET"])
@role_required('moderator')
def lectures_from_teacher(request, user_id):
    user = get_object_or_404(CustomUser, pk=user_id)
    lectures = Lecture.objects.filter(user=user).order_by('date', 'start')
    return Response({'lectures': LectureSerializer(lectures, many=True).data})


# localhost:8080/moderation/users/<user_id>/auditoriums/<auditorium_id>
# {}
@api_view(["POST", "DELETE"])
@role_required("moderator")
def manage_allowed_auditorium(request, user_id, auditorium_id):
    if request.method == "POST":
        auditorium = get_object_or_404(Auditorium, pk=auditorium_id)
        user = get_object_or_404(CustomUser, pk=user_id)
        if auditorium not in user.allowed_auditoriums.all():
            user.allowed_auditoriums.add(auditorium)
            user.save()
        return Response(status=status.HTTP_200_OK)
    elif request.method == "DELETE":
        user = get_object_or_404(CustomUser, pk=user_id)
        auditorium = get_object_or_404(Auditorium, pk=auditorium_id)
        user.allowed_auditoriums.remove(auditorium)
        user.save()
        return Response(status=status.HTTP_200_OK)


# localhost:8080/moderation/users/<user_id>/auditoriums
@api_view(["DELETE"])
@role_required("moderator")
def reset_allowed_auditoriums(request, user_id):
    user = get_object_or_404(CustomUser, pk=user_id)
    user.allowed_auditoriums.clear()
    user.save()
    return Response(status=status.HTTP_200_OK)


# localhost:8080/moderation/users/<user_id>/limit/hours
# {"amount": 1}
@api_view(["PATCH"])
@role_required("moderator")
def limit_amount_of_hours(request):
    user = utils.get_user_from_request(request)
    amount = request.data.get('amount')
    if amount >= 0:
        user.hours_limit = amount
        user.save()
        return Response(status=status.HTTP_200_OK)
    return Response(status=status.HTTP_400_BAD_REQUEST)


# localhost:8080/moderation/users/<user_id>/limit/auditoriums
# {"amount": 1}
@api_view(["PATCH"])
@role_required("moderator")
def limit_amount_of_auditoriums(request):
    user = utils.get_user_from_request(request)
    amount = request.data.get('amount')
    if amount >= 0:
        user.booking_limit = amount
        user.save()
        return Response(status=status.HTTP_200_OK)
    return Response(status=status.HTTP_400_BAD_REQUEST)
