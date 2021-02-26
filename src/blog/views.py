from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView
from .models import Post, Tag
from .forms import CreatePostForm


class PostListView(ListView):
    queryset = Post.objects.published()
    context_object_name = "posts"
    paginate_by = 3

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tags"] = Tag.objects.all()
        return context


class PostDetailView(DetailView):
    model = Post

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tags"] = Tag.objects.all()
        return context


def blog_tag(request, id):
    tag = Tag.objects.get(pk=id)
    posts = Post.objects.filter(tags__name__contains=tag.name).published()
    context = {"tag": tag, "posts": posts}
    return render(request, "blog/post_tag.html", context)


class PostListCreateView(ListView, CreateView):
    form_class = CreatePostForm
    template_name = "posts-management.html"

    def get(self, request, *args, **kwargs):
        author = self.request.user
        posts = Post.objects.filter(author=author)
        form = self.form_class()
        return render(request, self.template_name, {"form": form, "posts": posts})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        author = self.request.user
        if form.is_valid():
            title = form.cleaned_data.get("title")
            content = form.cleaned_data.get("content")
            published = form.cleaned_data.get("published")
            post = Post(
                title=title, content=content, published=published, author=author
            )
            post.save()
            return redirect("blog:posts-management")

        return render(request, self.template_name, {"form": form})
