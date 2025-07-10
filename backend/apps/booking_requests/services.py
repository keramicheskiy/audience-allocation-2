from apps.authentication.tasks import send_mail
from .models import BookingRequest


def notify_request_expired(request: BookingRequest):
    send_mail.delay(request.user.email, "Заявка автоматически отклонена", "К сожалению, ни один модератор не успел подтвердить вашу заявку.")


def notify_booking_request_declined(request: BookingRequest):
    send_mail.delay(request.user.email, "Заявка отклонена", "Ваша заявка была отклонена модератором.")


def notify_booking_request_accepted(request: BookingRequest):
    send_mail.delay(request.user.email, "Заявка подтверждена", "Ваша заявка была подтверждена модератором.")


