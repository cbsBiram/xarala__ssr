from celery import shared_task
from send_mail.views import enroll_course_mail


@shared_task
def enroll_course(student_email, course, order):
    mail_sent = enroll_course_mail(student_email, course, order)
    return mail_sent
