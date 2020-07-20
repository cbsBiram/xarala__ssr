from django.shortcuts import render, redirect
from blog.models import Post
from xarala.utils import SendSubscribeMail
from .models import Subscribe, Carousel, Team
from django.http import HttpResponse, JsonResponse
from django.views.generic import TemplateView, CreateView
from course.models import Course, Category
from .forms import ContactForm, BecomeTeacherForm

from send_mail.views import become_teacher_mail


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
    form_class = BecomeTeacherForm
    template_name = "pages/become-teacher.html"

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(
            request, self.template_name, {"form": form, "title": "Devenez instructeur"}
        )

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get("email")
            message = form.cleaned_data.get("message")
            form.save()
            become_teacher_mail(email, message)
            return redirect("pages:thanks")

        return render(request, self.template_name, {"form": form})
