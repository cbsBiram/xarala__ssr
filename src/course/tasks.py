from celery import task
from send_mail.views import enroll_course_mail


@task
def enroll_course(student_email, course, order):
    mail_sent = enroll_course_mail(student_email, course, order)
    return mail_sent
