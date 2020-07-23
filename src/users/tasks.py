from celery import shared_task
from send_mail.views import send_new_register_email


@shared_task
def account_created(email):
    mail_sent = send_new_register_email(email)
    return mail_sent
