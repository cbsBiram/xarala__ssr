from celery import shared_task
from send_mail.views import send_new_register_email, passowrd_reset_mail


@shared_task
def account_created(email):
    mail_sent = send_new_register_email(email)
    return mail_sent


@shared_task
def send_password_reset_email(email):
    mail_sent = passowrd_reset_mail(email)
    return mail_sent
