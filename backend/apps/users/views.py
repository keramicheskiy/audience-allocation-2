from django.shortcuts import render, get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from apps.auditoriums.models import Auditorium
from apps.auditoriums.serializers import AuditoriumSerializer
from apps.authentication import utils
from apps.authentication.decorators import role_required
from apps.authentication.models import CustomUser
from apps.authentication.serializers import CustomUserSerializer
from apps.lectures.models import Lecture
from apps.lectures.serializers import LectureSerializer
from apps.role_approvance_requests.models import RoleForApproving


# localhost:8080/users/<user_id>/lectures
@api_view(["GET"])
@role_required('moderator')
def lectures_from_teacher(request, user_id):
    user = get_object_or_404(CustomUser, pk=user_id)
    lectures = Lecture.objects.filter(user=user).order_by('date', 'start')
    return Response({'lectures': LectureSerializer(lectures, many=True).data})


# localhost:8080/users/<user_id>/auditoriums
# {"auditorium_id": 1}
@api_view(["GET", "POST", "DELETE"])
@role_required("moderator")
def get_allowed_auditoriums(request, user_id):
    if request.method == "GET":
        user = get_object_or_404(CustomUser, pk=user_id)
        return Response({"auditoriums": AuditoriumSerializer(user.allowed_auditoriums.all(), many=True).data})
    elif request.method == "POST":
        auditorium_id = request.data.get("auditorium_id")
        auditorium = get_object_or_404(Auditorium, pk=auditorium_id)
        user = get_object_or_404(CustomUser, pk=user_id)
        if auditorium not in user.allowed_auditoriums.all():
            user.allowed_auditoriums.add(auditorium)
            user.save()
        return Response(status=status.HTTP_201_CREATED)
    elif request.method == "DELETE":
        auditorium_id = request.data.get("auditorium_id")
        user = get_object_or_404(CustomUser, pk=user_id)
        auditorium = get_object_or_404(Auditorium, pk=auditorium_id)
        user.allowed_auditoriums.remove(auditorium)
        user.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


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
def limit_amount_of_hours(request, user_id):
    amount = int(request.data.get('amount'))
    if amount >= 0:
        user = get_object_or_404(CustomUser, pk=user_id)
        user.hours_limit = amount
        user.save()
        return Response(status=status.HTTP_200_OK)
    return Response(status=status.HTTP_400_BAD_REQUEST)


# localhost:8080/users/<user_id>/limit/auditoriums
# {"amount": 1}
@api_view(["PATCH"])
@role_required("moderator")
def limit_amount_of_auditoriums(request, user_id):
    amount = int(request.data.get('amount'))
    if amount >= 0:
        user = get_object_or_404(CustomUser, pk=user_id)
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
@api_view(["GET", "PATCH"])
@role_required("teacher")
def manage_user(request, user_id):
    user = get_object_or_404(CustomUser, pk=user_id)
    if request.method == "GET":
        return Response({"user": CustomUserSerializer(user).data}, status=status.HTTP_200_OK)
    elif request.method == "PATCH":
        curr_user = utils.get_user_from_request(request)
        if user != curr_user:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        data = request.data.copy()
        role_to_assign = data.pop("role", None)
        serializer = CustomUserSerializer(user, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            if role_to_assign:
                RoleForApproving.objects.get_or_create(user=curr_user, wannabe_role=role_to_assign)
            return Response({"user": serializer.data}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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


# localhost:8080/users/<user_id>/wannabe
@api_view(["GET"])
@role_required("admin")
def get_wannabe(request, user_id):
    user = get_object_or_404(CustomUser, pk=user_id)
    if RoleForApproving.objects.filter(user=user).exists():
        return Response({"role": RoleForApproving.objects.get(user=user).wannabe_role})
    return Response(status=status.HTTP_404_NOT_FOUND)
