from django import forms
from .models import (Course, Language, BEGINNER, MEDIUM, INTERMEDIATE)

LEVEL = (
        (BEGINNER, BEGINNER),
        (MEDIUM, MEDIUM),
        (INTERMEDIATE, INTERMEDIATE)
)


class CreateCourse(forms.ModelForm):
    title = forms.CharField(
        max_length=254,
        label='Titre de la formation',
        widget=forms.TextInput(
              {'placeholder': 'Titre'}))
    level = forms.ChoiceField(
        choices=LEVEL,
        label='Niveau')
    language = forms.ModelChoiceField(
        queryset=Language.objects.all(),
        label='Langue de la formation')
    published = forms.BooleanField(
        label='Publié',
        required=False
    )

    class Meta:
        model = Course
        fields = ("title", "level", "published",
                  "language", "description", "thumbnail")
