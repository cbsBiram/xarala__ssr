from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template, render_to_string
from django.conf import settings
from weasyprint import CSS, HTML
from datetime import datetime
from io import BytesIO

from users.models import ResetCode

# email apres la creation de compte


def send_new_register_email(email):
    htmly = get_template("email/thanks_new_register.html")
    context = {"email": email}
    to_emails = [
        email,
    ]
    subject, from_email = ("Bienvenue chez Xarala", "contact@xarala.co")
    html_content = htmly.render(context)
    msg = EmailMultiAlternatives(
        subject,
        html_content,
        from_email,
        to_emails,
    )
    msg.attach_alternative(
        html_content,
        "text/html",
    )
    msg.send(fail_silently=False)


def become_teacher_mail(email, message):
    htmly = get_template("email/become-teacher.html")
    context = {"email": email, "message": message}
    to_emails = [
        email,
        "xaralaxarala@gmail.com",
    ]
    subject, from_email = ("Xarala - Devenir instructeur", "contact@xarala.co")
    html_content = htmly.render(context)
    msg = EmailMultiAlternatives(
        subject,
        html_content,
        from_email,
        to_emails,
    )
    msg.attach_alternative(
        html_content,
        "text/html",
    )
    msg.send(fail_silently=False)


def enroll_course_mail(student_email, course_title):
    htmly = get_template("email/enroll_course.html")
    context = {"student_name": student_email, "course_title": course_title}
    to_emails = [student_email]
    subject, from_email = (f"Xarala -{course_title}", "contact@xarala.co")
    today = datetime.today()
    html_content = htmly.render(context)
    msg = EmailMultiAlternatives(
        subject,
        html_content,
        from_email,
        to_emails,
    )
    msg.attach_alternative(
        html_content,
        "text/html",
    )
    pdf_context = {"course_title": course_title, "invoice_date": today}
    html = render_to_string("invoice/enrolled_invoice.html", pdf_context)
    out = BytesIO()
    static_dir = (
        settings.STATICFILES_DIRS[0] if settings.DEBUG else settings.STATIC_ROOT
    )
    stylesheets = [CSS(static_dir + "/assets/css/pdf.css")]
    HTML(string=html).write_pdf(out, stylesheets=stylesheets)
    msg.attach(
        "facture_{}.pdf".format(course_title),
        out.getvalue(),
        "application/pdf",
    )
    msg.send(fail_silently=False)


def passowrd_reset_mail(user_email):
    htmly = get_template("email/passowrd_reset.html")
    code = ResetCode.objects.create(email=user_email)
    code.save()
    context = {"email": user_email, "code": code.code}
    to_emails = [user_email]
    subject, from_email = (
        "Xarala - réinitialisation mot de passe",
        "contact@xarala.co",
    )
    html_content = htmly.render(context)
    msg = EmailMultiAlternatives(
        subject,
        html_content,
        from_email,
        to_emails,
    )
    msg.attach_alternative(
        html_content,
        "text/html",
    )
    msg.send(fail_silently=False)
