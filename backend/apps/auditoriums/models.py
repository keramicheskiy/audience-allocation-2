from datetime import datetime

from django.db import models

from apps.equipments.models import Equipment


class Auditorium(models.Model):
    number = models.CharField(max_length=10)
    size = models.IntegerField(null=False, default=0)
    equipment = models.ForeignKey(Equipment, null=True, on_delete=models.SET_NULL)
    location = models.CharField(max_length=100, null=False, unique=False, default='')
    description = models.TextField(default="")

    def is_available(self, start: datetime, end: datetime):
        for lecture in self.lectures:
            if not (end <= lecture.start or start >= lecture.end):
                return False
        return True

    def __str__(self):
        return (f"Auditorium("
                f"id: {self.id}, "
                f"number: {self.number}, "
                f"size: {self.size}, "
                f"equipment: {self.equipment.name}, "
                f"location: {self.location}, "
                f"description: {self.description}"
                f")")
