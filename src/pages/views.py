from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.views.generic import CreateView, TemplateView

from blog.models import Post
from course.models import Category, Course
from users.tasks import account_created
from xarala.utils import SendSubscribeMail

from .forms import ContactForm, TeacherCreationForm
from .models import Carousel, Subscribe, Team
from userlogs.models import UserLog
from users.models import CustomUser


def home(request):
    course_counts = Course.objects.count()
    courses = Course.objects.order_by("-id")[:8]
    posts = Post.objects.order_by("-id")[:8]
    top_python = Course.objects.filter(
        categories__name__in=["Python", "Django", "Flask"]
    )
    top_developement = Course.objects.filter(
        categories__name__in=["Javascript", "React", "Développement Web", "Html", "Css"]
    )
    top_design = Course.objects.filter(
        categories__name__in=["Design", "Adobe XD", "Figma", "Sketch"]
    )
    categories = Category.objects.order_by("-id")
    carousel = Carousel.objects.last()
    return render(
        request,
        "pages/index.html",
        {
            "courses": courses,
            "top_python": top_python,
            "top_developement": top_developement,
            "top_design": top_design,
            "carousel": carousel,
            "categories": categories,
            "posts": posts,
            "course_counts": course_counts,
        },
    )


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
    return render(request, "pages/about.html")


def privacy_policy(request):
    return render(request, "pages/privacy_policy.html")


def faq(request):
    return render(request, "pages/faq.html")


def community_page(request):
    return render(request, "pages/community.html")


def team_page(request):
    teams = Team.objects.all()
    return render(request, "pages/team.html", {"teams": teams})


class ContactUsView(TemplateView, CreateView):
    form_class = ContactForm
    template_name = "pages/contact.html"

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(
            request, self.template_name, {"form": form, "title": "Nous contacter"}
        )

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            return redirect("pages:thanks")

        return render(request, self.template_name, {"form": form})


class ThanksView(TemplateView):
    template_name = "pages/thanks.html"


class BecomeTeacherView(TemplateView, CreateView):
    form_class = TeacherCreationForm
    template_name = "pages/become-instructor.html"

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
    return render(request, "pages/become-instructor.html")


class ShopHomePage(TemplateView):
    template_name = "shop/product_list.html"
