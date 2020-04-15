from django import forms
from .models import (Course, Chapter, Language, Lesson,
                     BEGINNER, MEDIUM, INTERMEDIATE,
                     YOUTUBE, VIMEO, CLOUDINARY, CUSTOM
                     )

LEVEL = (
        (BEGINNER, BEGINNER),
        (MEDIUM, MEDIUM),
        (INTERMEDIATE, INTERMEDIATE)
)

PLATFORM = (
    (YOUTUBE, YOUTUBE),
    (VIMEO, VIMEO),
    (CLOUDINARY, CLOUDINARY),
    (CUSTOM, CUSTOM)
)


class CreateCourse(forms.ModelForm):
    title = forms.CharField(
        max_length=254,
        label='Titre de la formation',
        widget=forms.TextInput(
              {'placeholder': 'Titre', 'class': ' border w-full py-2 px-3 text-grey-darker mt-2'}))
    level = forms.ChoiceField(
        choices=LEVEL,
        label='Niveau',
        widget=forms.Select(attrs={'class': 'form-select block w-full mt-1'}))
    language = forms.ModelChoiceField(
        queryset=Language.objects.all(),
        label='Langue de la formation',
        widget=forms.Select(attrs={'class': 'form-select block w-full mt-1'})
    )
    published = forms.BooleanField(
        label='Publié',
        required=False
    )
    description = forms.CharField(widget=forms.Textarea(
        attrs={'class': 'form-textarea mt-1 block w-full border', 'rows': '3'}))

    class Meta:
        model = Course
        fields = ("title", "level", "published",
                  "language", "description", "thumbnail")


class CreateChapter(forms.ModelForm):
    name = forms.CharField(
        max_length=254,
        label='Titre de la chapittre',
        widget=forms.TextInput(
              {'placeholder': 'Section 1 ou Introduction..',  'class': ' border w-full py-2 px-3 text-grey-darker mt-2'}))

    class Meta:
        model = Chapter
        fields = ("name",)


class CreateLesson(forms.ModelForm):
    title = forms.CharField(
        max_length=254,
        label='Titre de la chapittre',
        widget=forms.TextInput(
              {'placeholder': 'Cours..',  'class': ' border w-full py-2 px-3 text-grey-darker mt-2'}))
    text = forms.CharField(
        label="Description",
        widget=forms.Textarea(
            attrs={'class': 'form-textarea mt-1 block w-full border', 'rows': '3'}))
    video_id = forms.CharField(
        max_length=254,
        label='Video ID',
        widget=forms.TextInput(
              {'placeholder': 'Cours..',  'class': ' border w-full py-2 px-3 text-grey-darker mt-2'}))
    platform = forms.ChoiceField(
        choices=PLATFORM,
        label='Plateforme',
        widget=forms.Select(attrs={'class': 'form-select block w-full mt-1'}))

    class Meta:
        model = Lesson
        fields = ("title", "text", "video_id", "platform")
