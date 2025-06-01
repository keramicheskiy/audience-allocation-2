from django.db.models.signals import post_migrate
from django.dispatch import receiver

from apps.authentication import tasks
from apps.authentication.models import CustomUser
from backend import settings


@receiver(post_migrate)
def create_default_user(sender, **kwargs):
    if not CustomUser.objects.filter(email=settings.ADMIN_EMAIL).exists():
        user = CustomUser.objects.create_superuser(
            email=settings.ADMIN_EMAIL,
            password=settings.ADMIN_PASSWORD,
        )
        user.first_name = "Игнат"
        user.patronymic = "Петрович"
        user.last_name = "Шарков"
        user.is_verified = True
        user.save()

        tasks.send_telegram_message.delay(
            f"Суперпользователь {settings.ADMIN_EMAIL} {settings.ADMIN_PASSWORD} успешно создан.",
            settings.ADMIN_TG_ID
        )
