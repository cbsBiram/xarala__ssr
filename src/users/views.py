from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login
from django.contrib import messages
from .models import CustomUser
from .forms import CustomUserLoginForm


def login(request):
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
    if request.method == "POST":
        # Get form values
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        # check if password much
        if password == password2:
            pass
            # check username
            if CustomUser.objects.filter(email=email).exists():
                messages.error(request, "That email is taken")
                return redirect('register')
            else:
                if CustomUser.objects.filter(email=email).exists():
                    messages.error(request, "That email is being used")
                    return redirect('register')
                else:
                    # looks good
                    user = CustomUser.objects.create_user(
                        email=email,
                        password=password,
                    )
                    user.save()
                    messages.success(
                        request, "You are now registred and can log  in")
                    return redirect("login")
        else:
            messages.error(request, "Password didn't match")
            return redirect('register')
    else:
        context = {}
        return render(request, "users/register.html", context)
