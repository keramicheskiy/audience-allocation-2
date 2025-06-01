from django.core.management.base import BaseCommand

from apps.auditoriums.models import Auditorium
from apps.equipments.models import Equipment


class Command(BaseCommand):
    help = 'Создаёт оборудование и аудитории'

    def handle(self, *args, **kwargs):
        try:
            # Создаём оборудование
            nothing, _ = Equipment.objects.get_or_create(name='Ничего')
            projector, _ = Equipment.objects.get_or_create(name='Проектор')

            # Создаём аудитории и указываем оборудование
            Auditorium.objects.get_or_create(number='221B', equipment=nothing, size=300, location="ГУК В",
                                             description="...")
            Auditorium.objects.get_or_create(number='504А', equipment=projector, size=30, location="ГУК А",
                                             description="...")

            self.stdout.write(self.style.SUCCESS('✅ Оборудование и аудитории созданы!'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(e))
