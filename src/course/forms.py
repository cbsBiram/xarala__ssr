from django import forms
from django_summernote.widgets import SummernoteWidget
from .models import (
    Category,
    Course,
    Chapter,
    Language,
    Lesson,
    BEGINNER,
    MEDIUM,
    INTERMEDIATE,
    YOUTUBE,
    VIMEO,
    CLOUDINARY,
    CUSTOM,
)

LEVEL = ((BEGINNER, BEGINNER), (MEDIUM, MEDIUM), (INTERMEDIATE, INTERMEDIATE))

PLATFORM = (
    (YOUTUBE, YOUTUBE),
    (VIMEO, VIMEO),
    (CLOUDINARY, CLOUDINARY),
    (CUSTOM, CUSTOM),
)


class CreateCourse(forms.ModelForm):
    title = forms.CharField(
        max_length=254,
        label="Titre de la formation",
        required=True,
        error_messages={"required": "Le titre doit être renseigné."},
        widget=forms.TextInput(
            {
                "placeholder": "Titre",
                "class": "prompt srch_explore",
            }
        ),
    )
    description = forms.CharField(
        label="Description",
        required=True,
        error_messages={"required": "La description doit être renseignée."},
        widget=SummernoteWidget(
            attrs={"summernote": {"width": "100%", "height": "400px"}}
        ),
    )
    level = forms.ChoiceField(
        choices=LEVEL,
        label="Niveau",
        widget=forms.Select(
            attrs={"class": "ui hj145 dropdown cntry152 prompt srch_explore"}
        ),
    )
    language = forms.ModelChoiceField(
        queryset=Language.objects.all(),
        label="Langue de la formation",
        initial=Language.objects.first(),
        widget=forms.Select(
            attrs={"class": "ui hj145 dropdown cntry152 prompt srch_explore"}
        ),
    )
    categories = (
        forms.ModelMultipleChoiceField(
            queryset=Category.objects.all(),
            label="Catégories",
            required=True,
            initial=Category.objects.first(),
            widget=forms.SelectMultiple(
                attrs={"class": "ui hj145 dropdown cntry152 prompt srch_explore"}
            ),
        ),
    )
    price = forms.IntegerField(
        label="Titre de la formation",
        required=True,
        initial=0,
        widget=forms.NumberInput(
            {
                "placeholder": "Prix",
                "class": "prompt srch_explore",
            }
        ),
    )
    thumbnail = forms.FileField(
        label="Thumbnail",
        widget=forms.FileInput(
            {
                "class": "prompt srch_explore",
                "accept": "image/*",
            }
        ),
    )

    class Meta:
        model = Course
        fields = (
            "title",
            "level",
            "language",
            "categories",
            "price",
            "description",
            "thumbnail",
        )


class UpdateCourse(forms.ModelForm):
    title = forms.CharField(
        max_length=254,
        label="Titre de la formation",
        widget=forms.TextInput(
            {
                "class": "prompt srch_explore",
            }
        ),
    )
    description = forms.CharField(
        label="Description",
        widget=SummernoteWidget(
            attrs={"summernote": {"width": "100%", "height": "400px"}}
        ),
    )
    level = forms.ChoiceField(
        choices=LEVEL,
        label="Niveau",
        widget=forms.Select(
            attrs={"class": "ui hj145 dropdown cntry152 prompt srch_explore"}
        ),
    )
    language = forms.ModelChoiceField(
        queryset=Language.objects.all(),
        label="Langue de la formation",
        initial="Français - FR",
        widget=forms.Select(
            attrs={"class": "ui hj145 dropdown cntry152 prompt srch_explore"}
        ),
    )
    price = forms.IntegerField(
        label="Titre de la formation",
        initial=0,
        widget=forms.NumberInput(
            {
                "placeholder": "Prix",
                "class": "prompt srch_explore",
            }
        ),
    )
    thumbnail = forms.FileField(
        label="Thumbnail",
        widget=forms.FileInput(
            {
                "class": "prompt srch_explore",
                "accept": "image/*",
            }
        ),
    )

    class Meta:
        model = Course
        fields = ("title", "level", "language", "price", "description", "thumbnail")


class CreateChapter(forms.ModelForm):
    name = forms.CharField(
        max_length=254,
        required=True,
        label="Titre du chapitre",
        widget=forms.TextInput(
            {
                "class": "border w-full py-2 px-3 text-grey-darker mt-2",
            }
        ),
    )

    class Meta:
        model = Chapter
        fields = ("name",)


class UpdateChapter(forms.ModelForm):
    name = forms.CharField(
        max_length=254,
        label="Titre du chapitre",
        widget=forms.TextInput(
            {
                "class": "border w-full py-2 px-3 text-grey-darker mt-2",
            }
        ),
    )

    class Meta:
        model = Chapter
        fields = ("name",)


class CreateLesson(forms.ModelForm):
    title = forms.CharField(
        max_length=254,
        label="Titre de la leçon",
        widget=forms.TextInput(
            {
                "placeholder": "Cours..",
                "class": " border w-full py-2 px-3 text-grey-darker mt-2",
            }
        ),
    )
    text = forms.CharField(
        label="Description",
        widget=SummernoteWidget(),
    )
    # widget=forms.Textarea(
    # attrs={'class': 'form-textarea mt-1 block w-full border', 'rows': '3'})
    video_id = forms.CharField(
        max_length=254,
        label="URL de YouTube",
        widget=forms.TextInput(
            {
                "placeholder": "Leçon...",
                "class": " border w-full py-2 px-3 text-grey-darker mt-2",
            }
        ),
    )
    platform = forms.ChoiceField(
        choices=PLATFORM,
        label="Plateforme",
        widget=forms.Select(attrs={"class": "form-select block w-full mt-1"}),
    )

    class Meta:
        model = Lesson
        fields = ("title", "text", "video_id", "platform")


class UpdateLesson(forms.ModelForm):
    title = forms.CharField(
        max_length=254,
        label="Titre de la leçon",
        widget=forms.TextInput(
            {
                "placeholder": "Leçon...",
                "class": " border w-full py-2 px-3 text-grey-darker mt-2",
            }
        ),
    )
    text = forms.CharField(
        label="Description",
        widget=SummernoteWidget(),
    )
    # widget=forms.Textarea(
    # attrs={'class': 'form-textarea mt-1 block w-full border', 'rows': '3'})
    video_id = forms.CharField(
        max_length=254,
        label="URL de YouTube",
        widget=forms.TextInput(
            {
                "placeholder": "Cours..",
                "class": " border w-full py-2 px-3 text-grey-darker mt-2",
            }
        ),
    )
    platform = forms.ChoiceField(
        choices=PLATFORM,
        label="Plateforme",
        widget=forms.Select(attrs={"class": "form-select block w-full mt-1"}),
    )

    class Meta:
        model = Lesson
        fields = ("title", "text", "video_id", "platform")