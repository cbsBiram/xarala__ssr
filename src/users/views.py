from django.shortcuts import render, redirect
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import authenticate, login as auth_login
from django.contrib import messages
from django.utils.http import is_safe_url
from django.http import JsonResponse
from django.views.generic import UpdateView, DetailView

from course.models import Course
from .models import CustomUser
from .forms import (
    CustomUserUpdateForm,
    UpdateProfileForm,
    ChangePasswordForm,
    UpdateSocialForm,
    UpdateBioForm,
)
from send_mail.views import send_new_register_email
from userlogs.models import UserLog


def login(request):
    next_ = request.GET.get("next")
    next_post = request.POST.get("next")
    redirect_path = next_ or next_post if next_ or next_post else "/"
    if request.user.is_authenticated:
        return redirect("dashboard:dashboard")
    else:
        if request.method == "POST":
            next_ = request.GET.get("next")
            next_post = request.POST.get("next")
            redirect_path = next_ or next_post
            email = request.POST["email"]
            mail_to_lower = email.lower()
            password = request.POST["password"]
            user = authenticate(request, email=mail_to_lower, password=password)
            if user is not None:
                auth_login(request, user)
                if is_safe_url(redirect_path, request.get_host()):
                    return redirect(redirect_path)
                else:
                    return redirect("/")
            else:
                messages.error(request, "Information incorrect")
                UserLog.objects.create(
                    action=f"{email} Have problem to login", user_type="None", user=None
                )
                if redirect_path:
                    return redirect(f"/users/login/?next={redirect_path}")
                else:
                    return redirect("/users/login/")
        else:
            return render(request, "users/login.html", {"next": next_})


def register(request):
    next_ = request.GET.get("next")
    next_post = request.POST.get("next")
    redirect_path = next_ or next_post if next_ or next_post else "/"
    if request.user.is_authenticated:
        return redirect("dashboard:dashboard")
    else:
        if request.method == "POST":
            # Get form values
            email = request.POST["email"]
            mail_to_lower = email.lower()
            password = request.POST["password"]
            password2 = request.POST["password2"]
            # check if password much
            if password == password2:
                if CustomUser.objects.filter(email=mail_to_lower).exists():
                    messages.error(request, "Cet Email est déja utilisé")
                    return redirect(f"/users/register/?next={redirect_path}")
                else:
                    # looks good
                    user = CustomUser.objects.create_user(
                        email=mail_to_lower, password=password, is_student=True
                    )
                    user.save()
                    send_new_register_email(user)
                    user = authenticate(request, email=mail_to_lower, password=password)
                    if user is not None:
                        auth_login(request, user)
                    UserLog.objects.create(
                        action="Created account", user_type="Student", user=user
                    )
                    messages.success(request, "Compte crée avec succes...")
                    if is_safe_url(redirect_path, request.get_host()):
                        return redirect(redirect_path)
                    else:
                        return redirect("/")
            else:
                messages.error(request, "Les mots de passe ne sont pas identiques")
                return redirect(f"/users/register/?next={redirect_path}")
        else:
            return render(request, "users/register.html", {"next": next_})


# update user


class CustomUserUpdateDetailView(UpdateView, DetailView):
    model = CustomUser
    form_class = CustomUserUpdateForm
    avatar_form = UpdateProfileForm
    password_form = ChangePasswordForm
    social_form = UpdateSocialForm
    bio_form = UpdateBioForm
    template_name = "users/profile.html"

    def get(self, request, *args, **kwargs):
        user = request.user
        form = self.form_class(instance=user)
        avatar_form = self.avatar_form(instance=user)
        password_form = self.password_form(user=user)
        social_form = self.social_form(instance=user)
        bio_form = self.bio_form(instance=user)
        courses = Course.objects.all()
        if user.is_student:
            courses = user.courses_enrolled.all()
        elif user.is_teacher:
            courses = user.courses_created.all()

        return render(
            request,
            self.template_name,
            {
                "form": form,
                "user": user,
                "courses": courses,
                "avatar_form": avatar_form,
                "password_form": password_form,
                "social_form": social_form,
                "bio_form": bio_form,
            },
        )

    def post(self, request, *args, **kwargs):
        user = request.user
        form = self.form_class(request.POST, instance=user)
        password_form = self.password_form(request.POST, user=user)
        social_form = self.social_form(request.POST, instance=user)
        bio_form = self.bio_form(request.POST, instance=user)
        avatar_form = self.avatar_form(
            request.POST or None, request.FILES or None, instance=user
        )
        if request.is_ajax():
            pass
        return render(
            request,
            self.template_name,
            {
                "form": form,
                "avatar_form": avatar_form,
                "password_form": password_form,
                "social_form": social_form,
                "bio_form": bio_form,
            },
        )


def update_profile_image(request):
    avatar_form = UpdateProfileForm(
        request.POST or None, request.FILES or None, instance=request.user
    )
    try:
        if request.is_ajax() and avatar_form.is_valid():
            avatar = avatar_form.save(commit=False)
            avatar.save()
            return JsonResponse(
                {"code": "201", "message": "Profile mis a jour", "is_success": True}
            )
    except Exception as e:
        print(e)
        return JsonResponse(
            {"code": "500", "message": "Une erreur s'est produite", "is_success": False}
        )


def update_personal_info(request):
    personal_form = CustomUserUpdateForm(request.POST or None, instance=request.user)
    try:
        if request.is_ajax() and personal_form.is_valid():
            personal_info = personal_form.save(commit=False)
            personal_info.save()
            return JsonResponse(
                {"code": "201", "message": "Information mis a jour", "is_success": True}
            )
    except Exception as e:
        print(e)
        return JsonResponse(
            {"code": "500", "message": "Une erreur s'est produite", "is_success": False}
        )


def update_password(request):
    user = request.user
    password_form = PasswordChangeForm(user, request.POST)
    try:
        if request.is_ajax() and password_form.is_valid():
            password = password_form.save(commit=False)
            password.save()
            update_session_auth_hash(request, user)
            return JsonResponse(
                {
                    "code": "201",
                    "message": "Mot de passe mis a jour",
                    "is_success": True,
                }
            )
        return JsonResponse(
            {"errors": password_form.errors.as_json(), "is_error": True}
        )
    except Exception as e:
        print(e)
        return JsonResponse(
            {"code": "500", "message": "Une erreur s'est produite", "is_success": False}
        )


def update_social(request):
    social_form = UpdateSocialForm(request.POST or None, instance=request.user)
    try:
        if social_form.is_valid():
            social = social_form.save(commit=False)
            social.save()
            return JsonResponse(
                {
                    "code": "201",
                    "message": "Information sociale mis a jour",
                    "is_success": True,
                }
            )
    except Exception as e:
        print(e)
        return JsonResponse(
            {"code": "500", "message": "Une erreur s'est produite", "is_success": False}
        )


def update_bio(request):
    bio_form = UpdateBioForm(request.POST or None, instance=request.user)
    try:
        if bio_form.is_valid():
            bio = bio_form.save(commit=False)
            bio.save()
            return JsonResponse(
                {
                    "code": "201",
                    "message": "Information bio mis a jour",
                    "is_success": True,
                }
            )
    except Exception as e:
        print(e)
        return JsonResponse(
            {"code": "500", "message": "Une erreur s'est produite", "is_success": False}
        )
