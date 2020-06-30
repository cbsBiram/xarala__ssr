from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template


def become_teacher_mail(email, message):
    htmly = get_template("email/become-teacher.html")
    context = {"email": email, "message": message}
    to_emails = [
        email,
        "mstspr1155@gmail.com",
        "xaralaxarala@gmail.com",
    ]
    subject, from_email = ("Xarala - Devenir instructeur", "contact@xarala.tech")
    html_content = htmly.render(context)
    msg = EmailMultiAlternatives(subject, html_content, from_email, to_emails,)
    msg.attach_alternative(
        html_content, "text/html",
    )
    msg.send(fail_silently=False)
