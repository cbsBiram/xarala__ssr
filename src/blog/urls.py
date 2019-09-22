from django.urls import path
from . import views


urlpatterns = [
    path('', views.PostListView.as_view(), name="blog"),
    path('<slug:slug>/', views.PostDetailView.as_view(), name="blog-detail"),
    path("tags/<tag>/", views.blog_tag, name="blog_tag"),
]
