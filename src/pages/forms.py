from django import forms
from .models import Contact


RULES = (
    ("Étudiant", "Étudiant"),
    ("Instructeur", "Instructeur"),
    ("Incubateur", "Incubateur"),
    ("Autre", "Autre"),
)


class ContactForm(forms.ModelForm):
    first_name = forms.CharField(
        max_length=150,
        label="Nom complet",
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
        fields = ("first_name", "email", "phone", "message")


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
