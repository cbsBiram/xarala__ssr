from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm):
        model = CustomUser
        fields = ('email', 'avatar')


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ('email', 'avatar')


class CustomUserLoginForm(forms.Form):
    email = forms.CharField(
        max_length=254,
        label='Votre Email',
        widget=forms.TextInput(
            {'class': 'form-control', 'placeholder': 'Email'}))
    password = forms.CharField(
        label="Mot de passe",
        widget=forms.PasswordInput(
            {'class': 'form-control', 'placeholder': 'Mot de passe'})
    )
    # avatar = forms.ImageField()
