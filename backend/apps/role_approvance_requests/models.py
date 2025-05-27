from django.db import models
from django.db.models import OneToOneField

from apps.auth.models import CustomUser
from backend.settings import ROLES_CHOICES


class RoleForApproving(models.Model):
    user = OneToOneField(CustomUser, on_delete=models.CASCADE)
    wannabe_role = models.CharField(choices=ROLES_CHOICES, max_length=30)
