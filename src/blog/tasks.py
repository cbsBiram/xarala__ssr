from celery import task
from send_mail.views import send_author_submitted_email


@task
def author_submitted(email, post_title):
    mail_sent = send_author_submitted_email(email, post_title)
    return mail_sent
