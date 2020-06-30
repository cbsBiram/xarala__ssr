from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

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
    # avatar = forms.ImageField(label="Photo de profile", required=False,)
    email = forms.EmailField(
        label="Email",
        widget=forms.TextInput(
            attrs={
                "placeholder": "me@gmail.com",
                "class": "border w-full py-2 px-3 text-grey-darker mt-2",
                "disabled": "",
            }
        ),
    )
    first_name = forms.CharField(
        max_length=80,
        label="Prénom",
        widget=forms.TextInput(
            attrs={
                "placeholder": "Modou",
                "class": "border w-full py-2 px-3 text-grey-darker mt-2",
            }
        ),
    )
    last_name = forms.CharField(
        max_length=80,
        label="Nom",
        widget=forms.TextInput(
            attrs={
                "placeholder": "Diop",
                "class": "border w-full py-2 px-3 text-grey-darker mt-2",
            }
        ),
    )
    phone = forms.CharField(
        max_length=80,
        label="Numéro téléphone",
        widget=forms.TextInput(
            attrs={
                "placeholder": "778828878",
                "class": "border w-full py-2 px-3 text-grey-darker mt-2",
            }
        ),
    )
    address = forms.CharField(
        max_length=80,
        label="Adresse",
        widget=forms.TextInput(
            attrs={
                "placeholder": "Dakar, Senegal",
                "class": "border w-full py-2 px-3 text-grey-darker mt-2",
            }
        ),
    )
    bio = forms.CharField(
        label="Description",
        required=False,
        widget=forms.Textarea(
            attrs={"class": "form-textarea mt-1 block w-full border", "rows": "3"}
        ),
    )

    class Meta:
        model = CustomUser
        fields = ("email", "first_name", "last_name", "bio", "phone", "address")
