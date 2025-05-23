from datetime import datetime

from django.db import models

from apps.authentication.models import CustomUser
from apps.moderation.models import Subject, Auditorium
from backend.settings import tz
from bot import start


class Lecture(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    auditorium = models.ForeignKey(Auditorium, on_delete=models.CASCADE, related_name='lectures')
    start = models.DateTimeField()
    end = models.DateTimeField()

    def get_start_datetime(self) -> datetime:
        return self.start

    def get_end_datetime(self) -> datetime:
        return self.end


    def __str__(self):
        return (f"Lecture("
                f"id: {self.id}, "
                f"employee: {self.user}, "
                f"auditorium: {self.auditorium.number}, "
                f"start: {self.start}, "
                f"end: {self.end}"
                f")")
