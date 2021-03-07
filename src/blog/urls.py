from django.contrib.sitemaps.views import sitemap
from django.urls import path

from blog.sitemaps import PostSitemap

from . import views

app_name = "blog"
sitemaps = {"posts": PostSitemap}

urlpatterns = [
    path("", views.PostListView.as_view(), name="posts"),
    path("<slug:slug>/", views.PostDetailView.as_view(), name="blog-detail"),
    path("tutorials/tags/<str:tag_name>/", views.blog_tag, name="blog_tag"),
    path(
        "sitemap.xml",
        sitemap,
        {"sitemaps": sitemaps},
        name="django.contrib.sitemaps.views.sitemap",
    ),
]
