from rest_framework.decorators import api_view
from rest_framework.response import Response

from apps.auth.decorators import role_required
from apps.lectures.models import Lecture
from apps.lectures.serializers import LectureSerializer


# localhost:8080/lectures
@api_view(['GET'])
@role_required('moderator')
def get_lectures(request):
    lectures = Lecture.objects.all().order_by('date', 'start')
    return Response({'lectures': LectureSerializer(lectures, many=True).data})
