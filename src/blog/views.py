from django.shortcuts import render
from django.views.generic import ListView, DetailView, View
from .models import Post, Tag


class PostListView(ListView):
    model = Post
    context_object_name = 'posts'
    paginate_by = 2

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tags'] = Tag.objects.all()
        return context


class PostDetailView(DetailView):
    model = Post

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tags'] = Tag.objects.all()
        return context


def blog_tag(request, tag):
    posts = Post.objects.filter(
        tags__name__contains=tag
    ).order_by(
        '-date_created'
    )
    context = {
        "tag": tag,
        "posts": posts
    }
    return render(request, "blog/post_tag.html", context)
