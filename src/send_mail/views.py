from django.core.mail import EmailMultiAlternatives, send_mail, send_mass_mail
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from django.template.loader import get_template, render_to_string

# email apres la creation de compte


def send_new_register_email(user):
    htmly = get_template('email/thanks_new_register.html')
    context = {
        'user': user
    }
    to_emails = [
        user.email,
    ]
    subject, from_email = (
        'Merci d\'avoir utilisé Xarala',
        'mstspr1155@gmail.com'
    )
    html_content = htmly.render(context)
    msg = EmailMultiAlternatives(
        subject, html_content, from_email, to_emails, )
    msg.attach_alternative(html_content, "text/html",)
    msg.send(fail_silently=False)
