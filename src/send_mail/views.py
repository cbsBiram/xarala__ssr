from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template

# email apres la creation de compte


def send_new_register_email(email):
    htmly = get_template("email/thanks_new_register.html")
    context = {"email": email}
    to_emails = [
        email,
    ]
    subject, from_email = ("Bienvenue chez Xarala", "contact@xarala.co")
    html_content = htmly.render(context)
    msg = EmailMultiAlternatives(subject, html_content, from_email, to_emails,)
    msg.attach_alternative(
        html_content, "text/html",
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
    msg = EmailMultiAlternatives(subject, html_content, from_email, to_emails,)
    msg.attach_alternative(
        html_content, "text/html",
    )
    msg.send(fail_silently=False)
