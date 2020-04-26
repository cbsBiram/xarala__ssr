from django.shortcuts import render, redirect
from xarala.utils import SendSubscribeMail
from .models import Subscribe, Carousel, Contact
from django.http import HttpResponse, JsonResponse
from django.views.generic import TemplateView, CreateView
from course.models import Course
from blog.models import Post
from .forms import ContactForm


def home(request):
    courses = Course.objects.order_by('-id')[:4]
    posts = Post.objects.order_by('-id')[:4]
    carousel = Carousel.objects.last()
    return render(request, "pages/index.html", {"courses": courses, 'carousel': carousel, "posts": posts})


def subscribe(request):
    if request.method == 'POST':
        email = request.POST['email_id']
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


def community_page(request):
    return render(request, "pages/community.html")


class ContactUsView(TemplateView, CreateView):
    form_class = ContactForm
    template_name = "pages/contact.html"

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form, "title": "Nous contacter"})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        teacher = self.request.user
        if form.is_valid():
            form.save()
            return redirect('thanks')

        return render(request, self.template_name, {'form': form})


class ThanksView(TemplateView):
    template_name = "pages/thanks.html"
