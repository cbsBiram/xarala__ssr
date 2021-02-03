from celery import shared_task
from send_mail.views import send_author_submitted_email


@shared_task
def author_submitted(email, post_title):
    mail_sent = send_author_submitted_email(email, post_title)
    return mail_sent
