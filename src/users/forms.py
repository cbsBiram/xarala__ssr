from django import forms
from django.contrib.auth.forms import (
    UserCreationForm,
    UserChangeForm,
    PasswordChangeForm,
)

from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    password1 = forms.CharField(
        label="Mot de passe",
        widget=forms.PasswordInput(
            {
                "class": "border w-full py-2 px-3 text-grey-darker mt-",
                "placeholder": "Mot de passe",
            }
        ),
    )
    password2 = forms.CharField(
        label="Mot de passe",
        widget=forms.PasswordInput(
            {
                "class": "border w-full py-2 px-3 text-grey-darker mt-",
                "placeholder": "Mot de passe",
            }
        ),
    )

    class Meta(UserCreationForm):
        model = CustomUser
        fields = ("email", "password1")


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ("email", "avatar")


class CustomUserLoginForm(forms.Form):
    email = forms.CharField(
        max_length=254,
        label="Votre Email",
        widget=forms.TextInput(
            {
                "class": "border w-full py-2 px-3 text-grey-darker mt-",
                "placeholder": "Email",
            }
        ),
    )
    password = forms.CharField(
        label="Mot de passe",
        widget=forms.PasswordInput(
            {
                "class": "border w-full py-2 px-3 text-grey-darker mt-",
                "placeholder": "Mot de passe",
            }
        ),
    )
    # avatar = forms.ImageField()


class CustomUserProfileForm(forms.ModelForm):
    avatar = forms.ImageField(label="Photo de profile",)

    class Meta:
        model = CustomUser
        fields = ("avatar",)


class CustomUserUpdateForm(forms.ModelForm):
    email = forms.EmailField(label="Email")
    first_name = forms.CharField(max_length=80, label="Prénom")
    last_name = forms.CharField(max_length=80, label="Nom")
    phone = forms.CharField(max_length=80, label="Numéro de téléphone")
    address = forms.CharField(max_length=80, label="Adresse")
    title = forms.CharField(max_length=80, label="Titre")

    class Meta:
        model = CustomUser
        fields = (
            "first_name",
            "last_name",
            "email",
            "title",
            "phone",
            "address",
        )


class UpdateProfileForm(forms.ModelForm):
    avatar = forms.FileField(
        label="Photo de profile",
        widget=forms.FileInput(
            {
                "class": "opacity-0 position-absolute as-parent file-upload",
                "accept": "image/*",
            }
        ),
    )

    class Meta:
        model = CustomUser
        fields = ("avatar",)


class ChangePasswordForm(PasswordChangeForm):
    old_password = forms.CharField(
        max_length=80, label="Mot de passe actuel", widget=forms.PasswordInput()
    )
    new_password1 = forms.CharField(
        max_length=80, label="Nouveau mot de passe", widget=forms.PasswordInput()
    )
    new_password2 = forms.CharField(
        max_length=80, label="Confirmation mot de passe", widget=forms.PasswordInput()
    )

    class Meta:
        model = CustomUser


class UpdateSocialForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = (
            "facebook",
            "twitter",
            "linkedin",
            "github",
        )


class UpdateBioForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ("bio",)
