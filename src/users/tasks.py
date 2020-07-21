from celery import task
from send_mail.views import send_new_register_email


@task
def account_created(email):
    mail_sent = send_new_register_email(email)
    return mail_sent
