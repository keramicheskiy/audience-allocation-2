from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response

from apps.auth import utils
from apps.auth.decorators import role_required
from apps.lectures.models import Lecture
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
def get_upcoming_lectures(request):
    user = utils.get_user_from_request(request)
    upcoming_lectures = user.get_upcoming_lectures()
    return Response({'lectures': LectureSerializer(upcoming_lectures, many=True).data})
