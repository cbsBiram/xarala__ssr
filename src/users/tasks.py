from celery import task
from send_mail.views import send_new_register_email, passowrd_reset_mail


@task
def account_created(email):
    mail_sent = send_new_register_email(email)
    return mail_sent


@task
def send_password_reset_email(email):
    mail_sent = passowrd_reset_mail(email)
    return mail_sent
