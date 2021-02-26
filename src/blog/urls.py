from django.urls import path

from . import views

app_name = "blog"

urlpatterns = [
    path("", views.PostListView.as_view(), name="posts"),
    path("<slug:slug>/", views.PostDetailView.as_view(), name="blog-detail"),
    path("tags/<id>/", views.blog_tag, name="blog_tag"),
]
