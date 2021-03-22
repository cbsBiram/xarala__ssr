from celery import task
from send_mail.views import become_teacher_mail


@task
def become_teacher(email, message):
    mail_sent = become_teacher_mail(email, message)
    return mail_sent
