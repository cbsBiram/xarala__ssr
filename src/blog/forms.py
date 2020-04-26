from django import forms
from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget
from .models import Post


class CreatePostForm(forms.ModelForm):
    title = forms.CharField(
        max_length=254,
        label='Titre de l\'article',
        widget=forms.TextInput(
              {'placeholder': 'Tite..',  'class': ' border w-full py-2 px-3 text-grey-darker mt-2'}))
    content = forms.CharField(
        label="Description",
        widget=SummernoteWidget(),
    )
    image_url = forms.CharField(
        max_length=254,
        label='URL de l\'image',
        widget=forms.TextInput(
              {'placeholder': 'URL',  'class': ' border w-full py-2 px-3 text-grey-darker mt-2'}))

    class Meta:
        model = Post
        fields = ('title', 'content', 'image_url', 'published')
