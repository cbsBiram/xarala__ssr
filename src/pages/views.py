from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login
from django.http import HttpResponse, JsonResponse
from django.http.response import HttpResponseForbidden
from django.shortcuts import redirect, render
from django.views.generic import CreateView, TemplateView

from course.models import Course
from users.tasks import account_created
from xarala.utils import SendSubscribeMail

from .forms import ContactForm, TeacherCreationForm
from .models import Subscribe, Team
from userlogs.models import UserLog
from users.models import CustomUser


def home(request):
    return render(request, "index.html")


def subscribe(request):
    if request.method == "POST":
        email = request.POST["email_id"]
        email_qs = Subscribe.objects.filter(email_id=email)
        if email_qs.exists():
            data = {"status": "404"}
            return JsonResponse(data)
        else:
            Subscribe.objects.create(email_id=email)
            # Send the Mail, Class available in utils.py
            SendSubscribeMail(email)
    return HttpResponse("/")


def about(request):
    return render(request, "about.html")


def privacy_policy(request):
    return render(request, "privacy_policy.html")


def faq(request):
    return render(request, "faq.html")


def community_page(request):
    return render(request, "community.html")


def team_page(request):
    teams = Team.objects.all()
    return render(request, "team.html", {"teams": teams})


class ContactUsView(TemplateView, CreateView):
    form_class = ContactForm
    template_name = "contact.html"

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(
            request, self.template_name, {"form": form, "title": "Nous contacter"}
        )

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            # send mail
            return redirect("pages:thanks")

        return render(request, self.template_name, {"form": form})


class ThanksView(TemplateView):
    template_name = "thanks.html"


class BecomeTeacherView(TemplateView, CreateView):
    form_class = TeacherCreationForm
    template_name = "become-instructor.html"

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(
            request, self.template_name, {"form": form, "title": "Devenez instructeur"}
        )

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get("email")
            mail_to_lower = email.lower()
            password1 = form.cleaned_data.get("password1")
            password2 = form.cleaned_data.get("password2")
            if password1 != password2:
                messages.error(request, "Les mots de passe ne sont pas identiques")
                return redirect("pages:become-teacher")

            if password1 == password2:
                if CustomUser.objects.filter(email=mail_to_lower).exists():
                    messages.error(request, "Cet Email est déja utilisé")
                    return redirect("pages:become-teacher")
                else:
                    # looks good
                    teacher = CustomUser.objects.create_user(
                        email=mail_to_lower, password=password1, is_teacher=True
                    )
                    teacher.save()
                    account_created.delay(mail_to_lower)
                    user = authenticate(
                        request, email=mail_to_lower, password=password1
                    )
                    if user is not None:
                        auth_login(request, user)
                    UserLog.objects.create(
                        action="Created account", user_type="Teacher", user=user
                    )
                    messages.success(request, "Compte crée avec succes...")
                    return redirect("pages:thanks")
            else:
                messages.error(request, "Les mots de passe ne sont pas identiques")
                return redirect("pages:become-teacher")

        return render(request, self.template_name, {"form": form})


def teacher_registration(request):
    if request.method == "POST":
        email = request.POST.get("email")
        mail_to_lower = email.lower()
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")
        if password1 != password2:
            messages.error(request, "Les mots de passe ne sont pas identiques")
            return redirect("pages:become-teacher")
        if CustomUser.objects.filter(email=mail_to_lower).exists():
            messages.error(request, "Cet Email est déja utilisé")
            return redirect("pages:become-teacher")
        else:
            # looks good
            teacher = CustomUser.objects.create_user(
                email=mail_to_lower, password=password1, is_teacher=True
            )
            teacher.save()
            account_created.delay(mail_to_lower)
            user = authenticate(request, email=mail_to_lower, password=password1)
            if user is not None:
                auth_login(request, user)
            UserLog.objects.create(
                action="Created account", user_type="Teacher", user=user
            )
            messages.success(request, "Compte crée avec succes...")
            return redirect("dashboard:dashboard")
    return render(request, "become-instructor.html")
