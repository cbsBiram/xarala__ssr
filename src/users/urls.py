from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path("login/", views.login, name="login"),
    path("register/", views.register, name="register"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("profile/", views.CustomUserUpdateDetailView.as_view(), name="profile"),
    # change password
    path(
        "password_change/",
        auth_views.PasswordChangeView.as_view(
            template_name="users/change-password.html"
        ),
        name="password_change",
    ),
    path(
        "password_change/done/",
        auth_views.PasswordChangeDoneView.as_view(
            template_name="users/change-password-done.html"
        ),
        name="password_change_done",
    ),
    # reset password
    path(
        "password_reset/",
        auth_views.PasswordResetView.as_view(template_name="users/reset-password.html"),
        name="password_reset",
    ),
    path(
        "password_reset/done/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="users/reset-password-done.html"
        ),
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="users/reset-password-confirm.html"
        ),
        name="password_reset_confirm",
    ),
    path(
        "reset/done/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="users/reset-password-complete.html"
        ),
        name="password_reset_complete",
    ),
]
