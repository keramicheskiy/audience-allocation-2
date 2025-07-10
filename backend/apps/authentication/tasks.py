import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
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


