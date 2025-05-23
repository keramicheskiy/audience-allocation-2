from random import randint

from .models import VerifyCode, CustomUser
from .tasks import send_mail


def verify_email(user: CustomUser):
    code = str(randint(0, 9999)).zfill(4)
    text = (f"Для подтверждения регистрации введите в настройках аккаунта код: {code}.\n"
            f"Если вы не делали запрос на регистрацию, проигнорируйте данное письмо.")

    send_mail.delay(user.email, "Подтверждение регистрации", text)
    (verify_code, created) = VerifyCode.objects.get_or_create(user=user)
    verify_code.code = code
    verify_code.save()


def notify_moderators(user: CustomUser):
    text = (f"Пользователь {user.first_name} {user.patronymic} {user.last_name} ({user.email}) зарегестрировал "
            f"аккаунт и указал своей ролью {user.role}, подтвердите присвоение роли в панели модераторов.")
    send_mail.delay(user.email, "Новая регистрация", text)
