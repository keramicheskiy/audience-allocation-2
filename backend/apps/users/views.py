from django.shortcuts import render, get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from apps.auditoriums.models import Auditorium
from apps.authentication import utils
from apps.authentication.decorators import role_required
from apps.authentication.models import CustomUser
from apps.authentication.serializers import CustomUserSerializer
from apps.lectures.models import Lecture
from apps.lectures.serializers import LectureSerializer


# localhost:8080/users/<user_id>/lectures
@api_view(["GET"])
@role_required('moderator')
def lectures_from_teacher(request, user_id):
    user = get_object_or_404(CustomUser, pk=user_id)
    lectures = Lecture.objects.filter(user=user).order_by('date', 'start')
    return Response({'lectures': LectureSerializer(lectures, many=True).data})


# localhost:8080/users/<user_id>/auditoriums/<auditorium_id>
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


# localhost:8080/users/<user_id>/auditoriums
@api_view(["GET"])
@role_required("teacher")
def get_allowed_auditoriums(request, user_id):
    user = get_object_or_404(CustomUser, pk=user_id)
    return Response({"user": CustomUserSerializer(user).data})


# localhost:8080/users/<user_id>/auditoriums/reset
@api_view(["DELETE"])
@role_required("moderator")
def reset_allowed_auditoriums(request, user_id):
    user = get_object_or_404(CustomUser, pk=user_id)
    user.allowed_auditoriums.clear()
    user.save()
    return Response(status=status.HTTP_200_OK)


# localhost:8080/users/<user_id>/limit/hours
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


# localhost:8080/users/<user_id>/limit/auditoriums
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


# localhost:8080/users
@api_view(["GET"])
@role_required("moderator")
def get_users(request):
    users = CustomUser.objects.all()
    return Response({"users": CustomUserSerializer(users, many=True).data}, status=status.HTTP_200_OK)


# localhost:8080/users/<user_id>/role
# {"role": ""}
@api_view(['PATCH'])
@role_required("admin")
def change_role(request, user_id):
    user = get_object_or_404(CustomUser, pk=user_id)
    role = request.data.get('role')
    if not role:
        return Response({"detail": "Роль не указана."}, status=status.HTTP_400_BAD_REQUEST)
    new_role = user.assign_role(role)
    return Response({"role": new_role}, status=status.HTTP_200_OK)


# localhost:8080/users/{user_id}
@api_view(["GET"])
@role_required("teacher")
def get_user(request, user_id):
    user = get_object_or_404(CustomUser, pk=user_id)
    return Response({"users": CustomUserSerializer(user).data}, status=status.HTTP_200_OK)


# localhost:8080/users/<user_id>/delete
@api_view(["DELETE"])
@role_required("admin")
def delete_user(request, user_id):
    user = get_object_or_404(CustomUser, pk=user_id)
    user.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


# localhost:8080/users/<user_id>/lectures/<lecture_id>
@api_view(["DELETE"])
@role_required("moderator")
def delete_lecture(request, user_id, lecture_id):
    user = get_object_or_404(CustomUser, pk=user_id)
    lecture = get_object_or_404(Lecture, pk=lecture_id)
    if lecture.user == user:
        lecture.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    return Response(status=status.HTTP_404_NOT_FOUND)
