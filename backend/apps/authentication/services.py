from random import randint
from apps.authentication.models import VerifyCode, CustomUser
from apps.authentication.tasks import send_mail
from backend.settings import Roles


def verify_email(user: CustomUser):
    code = str(randint(0, 9999)).zfill(4)
    text = (f"Для подтверждения регистрации введите в настройках аккаунта код: {code}.\n"
            f"Если вы не делали запрос на регистрацию, проигнорируйте данное письмо.")
    verify_code, _ = VerifyCode.objects.get_or_create(user=user)
    verify_code.code = code
    verify_code.save()
    send_mail.delay(user.email, "Подтверждение регистрации", text)


def notify_moderators(user: CustomUser):
    text = (f"Пользователь {user.first_name} {user.patronymic} {user.last_name} ({user.email}) зарегестрировал "
            f"аккаунт и указал своей ролью {user.role}, подтвердите присвоение роли в панели модераторов.")
    for moderator in CustomUser.objects.filter(role__in=[Roles.ADMIN.value, Roles.MODERATOR.value]):
        send_mail.delay(moderator.email, "Новый пользователь", text)
