from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login
from django.contrib import messages
from .models import CustomUser
from .forms import CustomUserLoginForm
from send_mail.views import send_new_register_email


def login(request):
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
                messages.success(request, "Bienvenue chez Xarala")
                return redirect("/")
            else:
                messages.error(
                    request, "Information incorrect")
                return redirect('/users/login')
        else:
            return render(request, "users/login.html")


def register(request):
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
                    return redirect('register')
                else:
                    # looks good
                    user = CustomUser.objects.create_user(
                        email=email,
                        password=password,
                    )
                    user.save()
                    send_new_register_email(user)
                    messages.success(
                        request, "Vous êtes maintenant inscrit et pouvez vous connecter...")
                    return redirect("login")
            else:
                messages.error(
                    request, "Les mots de passe ne sont pas identiques")
                return redirect('register')
        else:
            return render(request, "users/register.html")


def dashboard(request):
    return render(request, "users/dashboard.html")