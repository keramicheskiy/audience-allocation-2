from django.core.management.base import BaseCommand

from apps.auditoriums.models import Auditorium
from apps.equipments.models import Equipment
from apps.buildings.models import Building
from apps.lectures.models import Lecture

from apps.authentication import serializers, services
from apps.authentication.models import CustomUser
from backend.settings import USERS_TO_CREATE

from apps.booking_requests.models import BookingRequest
import random
from datetime import datetime, timedelta
from backend.settings import time_zone

class Command(BaseCommand):
    help = 'Создаёт дэфолтные объекты'

    def handle(self, *args, **kwargs):
        self.create_users()
        equipments = self.create_equipments()
        buildings = self.create_buildings()
        auditoriums = self.create_auditoriums(buildings, equipments)
        self.create_booking_requests(auditoriums)
        self.create_lectures(auditoriums)
        
        self.stdout.write(self.style.SUCCESS('✅ Все данные успешно созданы ✅'))


    def create_users(self):
        """Создание пользователей"""
        for email in USERS_TO_CREATE.keys():
            if not CustomUser.objects.filter(email=email).exists():
                usr = USERS_TO_CREATE[email]
                usr["email"] = email
                serializer = serializers.CustomUserSerializer(data=usr)
                if serializer.is_valid():
                    user = serializer.save()
                    user.set_password(usr["password"])
                    user.assign_role(usr["role"])
                    user.is_verified = True
                    user.save()
                    services.verify_email(user)
                    services.notify_moderators(user)
                self.stdout.write(self.style.SUCCESS(f"✅ Пользователь {email} создан ✅"))


    def create_equipments(self):
        """Создание оборудования"""
        equipments = {
            'Ничего': Equipment.objects.get_or_create(name='Ничего')[0],
            'Проектор': Equipment.objects.get_or_create(name='Проектор')[0],
            'Стационарные компьютеры': Equipment.objects.get_or_create(name='Стационарные компьютеры')[0]
        }
        self.stdout.write(self.style.SUCCESS('✅ Оборудование создано'))
        return equipments


    def create_buildings(self):
        """Создание корпусов"""
        buildings = {
            'ГУК А': Building.objects.get_or_create(name="ГУК А")[0],
            'ГУК Б': Building.objects.get_or_create(name="ГУК Б")[0],
            'ГУК В': Building.objects.get_or_create(name="ГУК В")[0],
            'КОРПУС 5': Building.objects.get_or_create(name="КОРПУС 5")[0]
        }
        self.stdout.write(self.style.SUCCESS('✅ Корпуса созданы'))
        return buildings
    

    def create_auditoriums(self, buildings, equipments):
        """Создание аудиторий"""
        auditoriums = {
            '221B': Auditorium.objects.get_or_create(
                number='221B', size=300, building=buildings['ГУК В'],
                defaults={'description': "Большая аудитория без источников свежего воздуха."}
            )[0],
            '214B': Auditorium.objects.get_or_create(
                number='214B', size=300, building=buildings['ГУК В'],
                defaults={'description': "Большая аудитория без источников свежего воздуха."}
            )[0],
            '504A': Auditorium.objects.get_or_create(
                number='504А', size=30, building=buildings['ГУК А'],
                defaults={'description': "..."}
            )[0],
            'IT-17': Auditorium.objects.get_or_create(
                number='IT-17', size=40, building=buildings['ГУК А'],
                defaults={'description': "В аудитории есть 15 компьютеров."}
            )[0],
            '009': Auditorium.objects.get_or_create(
                number='009', size=20, building=buildings['КОРПУС 5'],
                defaults={'description': "Маленький класс в подвальном помещении."}
            )[0]
        }
        
        auditoriums['221B'].equipments.set([equipments['Проектор']])
        auditoriums['214B'].equipments.set([equipments['Ничего']])
        auditoriums['504A'].equipments.set([equipments['Проектор']])
        auditoriums['IT-17'].equipments.set([equipments['Стационарные компьютеры'], equipments['Проектор']])
        auditoriums['009'].equipments.set([equipments['Проектор']])
        
        self.stdout.write(self.style.SUCCESS('✅ Аудитории созданы'))
        return auditoriums
    

    def create_booking_requests(self, auditoriums):
        """Создание запросов на бронирование"""
        user1 = random.choice(CustomUser.objects.all() if CustomUser.objects.all().exists() else None)
        user2 = random.choice(CustomUser.objects.all() if CustomUser.objects.all().exists() else None)
        if not user1 or not user2:
            self.stdout.write(self.style.WARNING('⚠ Нет пользователей для создания бронирований'))
            return

        now = datetime.now(tz=time_zone)
        
        BookingRequest.objects.get_or_create(
            user=user1,
            auditorium=auditoriums['IT-17'],
            start=now + timedelta(hours=4),
            end=now + timedelta(hours=5, minutes=30)
        )
        
        BookingRequest.objects.get_or_create(
            user=user2,
            auditorium=auditoriums['504A'],
            start=now + timedelta(hours=2),
            end=now + timedelta(hours=3, minutes=30)
        )
        
        self.stdout.write(self.style.SUCCESS('✅ Запросы на бронирование созданы'))


    def create_lectures(self, auditoriums):
        """Создание лекций"""
        if Lecture.objects.all().exists():
            return
        user1 = random.choice(CustomUser.objects.all() if CustomUser.objects.all().exists() else None)
        user2 = random.choice(CustomUser.objects.all() if CustomUser.objects.all().exists() else None)
        if not user1 or not user2:
            self.stdout.write(self.style.WARNING('⚠ Нет пользователей для создания лекций'))
            return

        now = datetime.now(tz=time_zone)
        
        Lecture.objects.get_or_create(
            user=user1,
            auditorium=auditoriums['214B'],
            start=now + timedelta(hours=1),
            end=now + timedelta(hours=2, minutes=30)
        )
        
        Lecture.objects.get_or_create(
            user=user2,
            auditorium=auditoriums['IT-17'],
            start=now + timedelta(hours=6),
            end=now + timedelta(hours=7, minutes=30)
        )
        
        self.stdout.write(self.style.SUCCESS('✅ Лекции созданы'))

