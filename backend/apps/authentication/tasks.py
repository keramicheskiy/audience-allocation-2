import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

import requests
from celery import shared_task

from backend.settings import sender_email, email_password, smtp_server, smtp_port, TELEGRAM_BOT_TOKEN


@shared_task
def send_mail(receiver_email, subject, text):
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject

    message.attach(MIMEText(text, "plain"))

    try:
        server = smtplib.SMTP_SSL(smtp_server, smtp_port)
        server.login(sender_email, email_password)
        server.sendmail(sender_email, receiver_email, message.as_string())
        print("Письмо успешно отправлено!")
        return True
    except Exception as e:
        print(f"Ошибка отправки: {e}")
        return False

@shared_task
def send_telegram_message(message: str, tg_id: str):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": tg_id,
        "text": message,
        "parse_mode": "HTML"
    }
    try:
        response = requests.post(url, json=payload)
        return f"Отправлено: {message}"
    except Exception as e:
        print("Ошибка при отправке сообщения")


