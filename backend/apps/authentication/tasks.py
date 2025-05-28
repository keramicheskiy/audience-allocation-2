import smtplib
from datetime import time
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from time import sleep

from celery import shared_task

from backend.settings import sender_email, email_password, smtp_server, smtp_port


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


from celery import shared_task
import requests


TELEGRAM_BOT_TOKEN = "7844200914:AAFPCl39h-hGhqfpFhShyReSjRQXEBogyes"
TELEGRAM_USER_ID = 1212560164


@shared_task
def send_telegram_message(message: str):
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_USER_ID:
        raise ValueError("TELEGRAM_BOT_TOKEN или TELEGRAM_USER_ID не заданы")

    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_USER_ID,
        "text": message,
        "parse_mode": "HTML"
    }

    response = requests.post(url, json=payload)
    if response.status_code != 200:
        raise Exception(f"Ошибка при отправке: {response.text}")

    return f"Отправлено: {message}"
