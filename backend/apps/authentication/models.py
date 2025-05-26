from datetime import datetime

from django.contrib.auth.models import PermissionsMixin, User, AbstractBaseUser, BaseUserManager
from django.db import models
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

from apps.moderation.views import get_lectures
from apps.teachers.models import Auditorium, Lecture
from backend.settings import ROLES_CHOICES, ROLES, time_zone


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email is required')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('role', 'admin')
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)
        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    username = None  # Отключаем, преподы не осилят ники

    first_name = models.CharField(max_length=50, blank=True, null=True)
    patronymic = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=50, choices=ROLES_CHOICES, default='none', blank=True)
    is_verified = models.BooleanField(default=False)

    allowed_auditoriums = models.ManyToManyField(Auditorium, blank=True)
    booking_limit = models.PositiveIntegerField(default=10, blank=True, null=True)
    hours_limit = models.PositiveIntegerField(default=20, blank=True, null=True)

    is_staff = models.BooleanField(default=False)  # Для админки
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return f"{self.email} ({self.get_role_display()})"

    def assign_role(self, role):
        if role == "teacher":
            self.is_staff = False
            self.is_superuser = False
        elif role == "moderator":
            self.is_staff = True
            self.is_superuser = False
        elif role == "admin":
            self.is_staff = True
            self.is_superuser = True
        self.role = role if role in ROLES else "teacher"
        self.save()
        return self.role

    def get_upcoming_lectures(self):
        now = datetime.now(tz=time_zone)
        lectures = Lecture.objects.filter(email=self.email).order_by('date', 'start')
        not_yet_passed = []
        for lecture in lectures:
            lecture_end = lecture.end
            if lecture_end > now:
                not_yet_passed.append(lecture)
        return not_yet_passed

    def get_amount_of_seconds_booked(self):
        return sum(
            [(lecture.end - lecture.start).total_seconds() for lecture in self.get_upcoming_lectures()])

    def validate_booking_limit(self):
        if len(self.get_upcoming_lectures()) + 1 > self.booking_limit:
            return Response({"error": "Вы забронировали максимальное количество аудиторий."},
                            status=status.HTTP_403_FORBIDDEN)
        return None

    def validate_time_limit(self, start, end):
        if ((end - start).total_seconds() + self.get_amount_of_seconds_booked()) / 3600 > self.hours_limit:
            return Response({"error": "У вас кончились доступные вам часы для бронирования аудиторий."},
                            status=status.HTTP_403_FORBIDDEN)
        return None


class VerifyCode(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    code = models.CharField(max_length=10)
