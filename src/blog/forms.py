from django import forms
from django_summernote.widgets import SummernoteWidget
from .models import Post


class CreatePostForm(forms.ModelForm):
    title = forms.CharField(
        max_length=254,
        label="Titre de l'article",
        required=True,
        error_messages={"required": "Le titre doit être renseigné."},
        widget=forms.TextInput(
            {
                "placeholder": "Titre",
                "class": "prompt srch_explore",
            }
        ),
    )
    content = forms.CharField(
        label="Contenu",
        required=True,
        error_messages={"required": "Le contenu doit être rempli."},
        widget=SummernoteWidget(
            attrs={"summernote": {"width": "100%", "height": "400px"}}
        ),
    )
    description = forms.CharField(
        label="Description",
        widget=forms.TextInput(
            {
                "placeholder": "Petit résumé",
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
        model = Post
        fields = ("title", "content", "thumbnail", "description")


class UpdatePostForm(forms.ModelForm):
    title = forms.CharField(
        max_length=254,
        label="Titre de l'article",
        widget=forms.TextInput(
            {
                "placeholder": "Titre",
                "class": "prompt srch_explore",
            }
        ),
    )
    content = forms.CharField(
        label="Contenu",
        widget=SummernoteWidget(
            attrs={"summernote": {"width": "100%", "height": "400px"}}
        ),
    )
    description = forms.CharField(
        label="Description",
        widget=forms.TextInput(
            {
                "placeholder": "Petit résumé",
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
        model = Post
        fields = ("title", "content", "thumbnail", "description")
