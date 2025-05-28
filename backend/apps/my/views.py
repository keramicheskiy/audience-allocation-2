from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response

from apps.authentication import utils
from apps.authentication.decorators import role_required
from apps.authentication.serializers import CustomUserSerializer
from apps.lectures.models import Lecture, get_upcoming_lectures
from apps.lectures.serializers import LectureSerializer


# localhost:8080/my/lectures
@api_view(["GET"])
@role_required("teacher")
def get_own_lectures(request):
    user = utils.get_user_from_request(request)
    lectures = Lecture.objects.filter(email=user.email).order_by('date', 'start').all()
    return Response({"lectures": LectureSerializer(lectures, many=True).data}, status=status.HTTP_200_OK)


# localhost:8080/my/lectures/upcoming
@api_view(['GET'])
@role_required('teacher')
def get_my_upcoming_lectures(request):
    user = utils.get_user_from_request(request.user)
    upcoming_lectures = get_upcoming_lectures().filter(user=user)
    return Response({'lectures': LectureSerializer(upcoming_lectures, many=True).data})


# localhost:8080/my/profile
@api_view(['GET'])
@role_required('teacher')
def get_profile(request):
    user = utils.get_user_from_request(request)
    return Response({"user": CustomUserSerializer(user).data})
