from datetime import datetime

from django.db import models

from apps.moderation.models import Auditorium
from django.conf import settings

class Lecture(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    auditorium = models.ForeignKey(Auditorium, on_delete=models.CASCADE, related_name='lectures')
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
