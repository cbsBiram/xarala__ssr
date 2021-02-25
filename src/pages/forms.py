from django import forms
from django.contrib.auth.forms import UserCreationForm
from users.models import CustomUser
from .models import Contact


class ContactForm(forms.ModelForm):
    full_name = forms.CharField(
        max_length=150,
        label="Nom & prénom(s)",
        widget=forms.TextInput(
            {"placeholder": "Ex: John Diop", "class": "form-control"}
        ),
    )
    email = forms.EmailField(
        max_length=150,
        label="Email",
        widget=forms.EmailInput(
            {"placeholder": "monmail@gmail.com", "class": "form-control"}
        ),
    )
    phone = forms.CharField(
        max_length=150,
        label="Téléphone",
        widget=forms.TextInput(
            {"placeholder": "77 992 88 98", "class": "form-control"}
        ),
    )
    message = forms.CharField(
        label="Votre Message",
        widget=forms.Textarea(
            attrs={"class": "form-control", "rows": "7", "placeholder": "Votre message"}
        ),
    )

    class Meta:
        model = Contact
        fields = (
            "full_name",
            "email",
            "phone",
            "message",
        )


class BecomeTeacherForm(forms.ModelForm):
    first_name = forms.CharField(
        max_length=150,
        label="Nom Complet",
        widget=forms.TextInput(
            {"placeholder": "Ex: Modou Diop", "class": "form-control"}
        ),
    )
    email = forms.EmailField(
        max_length=150,
        label="Email",
        widget=forms.EmailInput(
            {"placeholder": "monmail@gmail.com", "class": "form-control"}
        ),
    )
    phone = forms.CharField(
        max_length=150,
        label="Téléphone(Whatsapp si possible)",
        widget=forms.TextInput(
            {"placeholder": "77 992 88 98", "class": "form-control"}
        ),
    )
    message = forms.CharField(
        label="Parlez-nous un peu de vous et de votre motivation pour enseigner sur Xarala",
        widget=forms.Textarea(
            attrs={"class": "form-control", "rows": "7", "placeholder": "Votre message"}
        ),
    )

    class Meta:
        model = Contact
        fields = ("first_name", "email", "phone", "message")


class TeacherCreationForm(UserCreationForm):
    password1 = forms.CharField(
        label="Mot de passe",
        widget=forms.PasswordInput(
            {
                "class": "form-control border-left-0 pl-0",
                "placeholder": "Mot de passe",
            }
        ),
    )
    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(
            {
                "class": "form-control border-left-0 pl-0",
                "placeholder": "moi@gmail.com",
            }
        ),
    )
    password2 = forms.CharField(
        label=False,
        widget=forms.PasswordInput(
            {
                "class": "form-control border-left-0 pl-0",
                "placeholder": "Confirmation Mot de passe",
            }
        ),
    )

    class Meta(UserCreationForm):
        model = CustomUser
        fields = ("email", "password1", "password2")
