from datetime import datetime

from django.db import models

from apps.equipments.models import Equipment
from apps.buildings.models import Building


class Auditorium(models.Model):
    number = models.CharField(max_length=10)
    size = models.IntegerField(null=False, default=1)
    equipments = models.ManyToManyField(Equipment, related_name="auditoriums")
    building = models.ForeignKey(Building, on_delete=models.SET_NULL, related_name="auditoriums", null=True, blank=True)
    description = models.TextField(default="", blank=True, null=True)

    def is_available(self, start: datetime, end: datetime):
        for lecture in self.lectures:
            if not (end <= lecture.start or start >= lecture.end):
                return False
        return True

    def __str__(self):
        return (f"Auditorium("
                f"id: {self.id}, "
                f"number: {self.number}, "
                f"size: {self.size} people, "
                f"equipment: {self.equipment.name}, "
                f"building: {self.building}, "
                f"description: {self.description}"
                f")")
