from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login
from django.contrib import messages
from django.utils.http import is_safe_url
from .models import CustomUser
from .forms import CustomUserLoginForm
from send_mail.views import send_new_register_email


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
                # messages.success(request, f"Bienvenue {user}, chez Xarala")
                if is_safe_url(redirect_path, request.get_host()):
                    return redirect(redirect_path)
                else:
                    return redirect("/")
            else:
                messages.error(
                    request, "Information incorrect")
                return redirect(f'/users/login/?next={redirect_path}')
        else:
            return render(request, "users/login.html", {"next": next_})


def register(request):
    next_ = request.GET.get('next')
    print("next ", next_)
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
                    messages.error(request, "Le email est deja utilisé")
                    return redirect(f'/users/register/?next={redirect_path}')
                else:
                    # looks good
                    user = CustomUser.objects.create_user(
                        email=email,
                        password=password,
                    )
                    user.save()
                    send_new_register_email(user)
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


# nouveau projet
@login_required(login_url="login")
def dashboard(request):
    student = request.user
    courses_enrolled = student.courses_enrolled.all().count()
    return render(
        request,
        "users/dashboard.html",
        {"student": student,
         "courses_enrolled": courses_enrolled}
    )
