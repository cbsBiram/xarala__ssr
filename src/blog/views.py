from django.shortcuts import render, redirect
from django.views.generic import (ListView, DetailView, View, CreateView)
from .models import Post, Tag
from .forms import CreatePostForm


class PostListView(ListView):
    # model = Post
    queryset = Post.objects.order_by('-date_published')
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


class PostListCreateView(ListView, CreateView):
    form_class = CreatePostForm
    template_name = "dashboard/posts-management.html"

    def get(self, request, *args, **kwargs):
        author = self.request.user
        posts = Post.objects.filter(author=author)
        form = self.form_class()
        return render(request, self.template_name, {'form': form, "posts": posts})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        author = self.request.user
        if form.is_valid():
            title = form.cleaned_data.get('title')
            content = form.cleaned_data.get('content')
            image_url = form.cleaned_data.get('image_url')
            published = form.cleaned_data.get('published')
            post = Post(
                title=title,
                content=content,
                published=published,
                author=author
            )
            post.save()
            return redirect('posts-management')

        return render(request, self.template_name, {'form': form})
