from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from apps.authentication import utils
from apps.authentication.decorators import role_required
from apps.lectures.models import Lecture, get_upcoming_lectures
from apps.lectures.serializers import LectureSerializer


# localhost:8080/lectures
@api_view(['GET'])
@role_required('moderator')
def get_lectures(request):
    lectures = Lecture.objects.all().order_by('start')
    return Response({'lectures': LectureSerializer(lectures, many=True).data})


# localhost:8080/lectures/upcoming
@api_view(['GET'])
@role_required('teacher')
def get_all_upcoming_lectures(request):
    upcoming_lectures = get_upcoming_lectures()
    return Response({'lectures': LectureSerializer(upcoming_lectures, many=True).data})


# localhost:8080/lectures/<lecture_id>
@api_view(["GET", "DELETE"])
@role_required('teacher')
def delete_lecture(request, lecture_id):
    if request.method == "GET":
        lecture = get_object_or_404(Lecture, pk=lecture_id)
        return Response({"lecture": LectureSerializer(lecture).data})
    elif request.method == "DELETE":
        user = utils.get_user_from_request(request.user)
        if user.lectures.filter(id=lecture_id).exists():
            Lecture.objects.get(id=lecture_id).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_404_NOT_FOUND)
