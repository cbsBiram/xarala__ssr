from django.core.mail import send_mail
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login
from django.contrib import messages
from django.utils.http import is_safe_url
from django.views.generic import TemplateView, UpdateView, DetailView
from .models import CustomUser
from .forms import (CustomUserLoginForm,
                    CustomUserUpdateForm,
                    CustomUserProfileForm,
                    CustomUserChangeForm)
from send_mail.views import send_new_register_email
from course.models import Course
from userlogs.models import UserLog


def login(request):
    next_ = request.GET.get('next')
    next_post = request.POST.get('next')
    redirect_path = next_ or next_post
    if request.user.is_authenticated:
        return redirect('dashboard')
    else:
        if request.method == "POST":
            next_ = request.GET.get('next')
            next_post = request.POST.get('next')
            redirect_path = next_ or next_post
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(request, email=email, password=password)
            if user is not None:
                auth_login(request, user)

                if is_safe_url(redirect_path, request.get_host()):
                    return redirect(redirect_path)
                else:
                    return redirect("/")
            else:
                messages.error(
                    request, "Information incorrect")
                UserLog.objects.create(
                    action=f'{email}Have problem to login',
                    user_type="None",
                    user=None)
                if redirect_path:
                    return redirect(f'/users/login/?next={redirect_path}')
                else:
                    return redirect("/users/login/")
        else:
            return render(request, "users/login.html", {"next": next_})


def register(request):
    next_ = request.GET.get('next')
    next_post = request.POST.get('next')
    redirect_path = next_ or next_post
    if request.user.is_authenticated:
        return redirect('dashboard')
    else:
        if request.method == "POST":
            # Get form values
            email = request.POST['email']
            password = request.POST['password']
            password2 = request.POST['password2']
            # check if password much
            if password == password2:
                if CustomUser.objects.filter(email=email).exists():
                    messages.error(request, "Cet Email est déja utilisé")
                    return redirect(f'/users/register/?next={redirect_path}')
                else:
                    # looks good
                    user = CustomUser.objects.create_user(
                        email=email,
                        password=password,
                    )
                    user.save()
                    send_new_register_email(user)
                    UserLog.objects.create(
                        action=f'Created account',
                        user_type=user.user_type,
                        user=user)
                    messages.success(
                        request, "compte crée avec succes...")
                    if is_safe_url(redirect_path, request.get_host()):
                        return redirect(redirect_path)
                    else:
                        return redirect("/")
            else:
                messages.error(
                    request, "Les mots de passe ne sont pas identiques")
                return redirect(f'/users/register/?next={redirect_path}')
        else:
            return render(request, "users/register.html", {"next": next_})


class AdminView(TemplateView):
    template_name = "dashboard/admin.html"
    total_courses = Course.objects.all().count()
    total_users = CustomUser.objects.all().count()
    total_students = CustomUser.objects.filter(user_type="ST").count()
    logs = UserLog.objects.all()[:3]

    extra_context = {
        'title': 'Staff',
        'total_courses': total_courses,
        'total_users': total_users,
        'total_students': total_students,
        'logs': logs,
    }

# update user


class CustomUserUpdateDetailView(UpdateView, DetailView):
    model = CustomUser
    form_class = CustomUserUpdateForm
    template_name = "users/profile.html"

    def get(self, request, *args, **kwargs):
        form = self.form_class(instance=request.user)

        return render(request, self.template_name, {
            'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(
            request.POST, instance=request.user)
        user = CustomUser.objects.filter(pk=request.user.id)
        if form.is_valid():
            form.save()
            return redirect('profile')
        return render(request, self.template_name, {'form': form})
