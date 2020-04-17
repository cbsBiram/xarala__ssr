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
        label='Votre Prénom',
        widget=forms.TextInput(
            {'placeholder': 'Ex: Modou',
             'class': 'appearance-none block w-full bg-gray-200 text-gray-700 border  rounded py-3 px-4 mb-3 leading-tight focus:outline-none focus:bg-white'}))
    last_name = forms.CharField(
        max_length=150,
        label='Votre Nom',
        widget=forms.TextInput(
            {'placeholder': 'Ex: Diop',
             'class': 'appearance-none block w-full bg-gray-200 text-gray-700 border  rounded py-3 px-4 mb-3 leading-tight focus:outline-none focus:bg-white'}))
    email = forms.EmailField(
        max_length=150,
        label='Email',
        widget=forms.EmailInput(
            {'placeholder': 'monmail@gmail.com',
             'class': 'appearance-none block w-full bg-gray-200 text-gray-700 border  rounded py-3 px-4 mb-3 leading-tight focus:outline-none focus:bg-white'}))
    phone = forms.CharField(
        max_length=150,
        label='Telephone',
        widget=forms.TextInput(
            {'placeholder': '77 992 88 98',
             'class': 'appearance-none block w-full bg-gray-200 text-gray-700 border  rounded py-3 px-4 mb-3 leading-tight focus:outline-none focus:bg-white'}))
    enterprise = forms.CharField(
        max_length=150,
        label='Enterprise ou École..',
        widget=forms.TextInput(
            {'placeholder': 'Ex: Xarala',
             'class': 'appearance-none block w-full bg-gray-200 text-gray-700 border  rounded py-3 px-4 mb-3 leading-tight focus:outline-none focus:bg-white'}))
    rule = forms.ChoiceField(
        choices=RULES,
        label='Votre rôle',
        widget=forms.Select(attrs={'class': 'form-select block w-full mt-1'}))
    message = forms.CharField(
        label="Description",
        required=False,
        widget=forms.Textarea(
            attrs={'class': 'no-resize appearance-none block w-full bg-gray-200 text-gray-700 border border-gray-200 rounded py-3 px-4 mb-3 leading-tight focus:outline-none focus:bg-white focus:border-gray-500 h-48 resize-none', 'rows': '3'}))

    class Meta:
        model = Contact
        fields = ('first_name', 'last_name', 'email',
                  'phone', 'rule', 'message')
