from datetime import datetime

from django.db import models
from django.conf import settings
from apps.auditoriums.models import Auditorium
from backend.settings import time_zone


def get_upcoming_lectures():
    now = datetime.now(tz=time_zone)
    lectures = Lecture.objects.order_by('start')
    not_yet_passed = []
    for lecture in lectures:
        if lecture.end > now:
            not_yet_passed.append(lecture)
    return not_yet_passed


class Lecture(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    auditorium = models.ForeignKey(Auditorium, on_delete=models.CASCADE, related_name='lectures', related_query_name='lecture')
    start = models.DateTimeField()
    end = models.DateTimeField()

    def __str__(self):
        return (f"Lecture("
                f"id: {self.id}, "
                f"employee: {self.user}, "
                f"auditorium: {self.auditorium.number}, "
                f"start: {self.start}, "
                f"end: {self.end}"
                f")")
