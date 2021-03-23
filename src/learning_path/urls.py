from django.urls import path
from . import views

app_name = "learning_path"

urlpatterns = [
    path("", views.LearningPathView.as_view(), name="paths"),
    path(
        "<slug:slug>/details/",
        views.LearningPathDetailView.as_view(),
        name="path-detail",
    ),
]
