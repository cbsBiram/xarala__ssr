from celery import shared_task
from send_mail.views import enroll_course_mail


@shared_task
def enroll_course(student_name, course_title):
    mail_sent = enroll_course_mail(student_name, course_title)
    return mail_sent
