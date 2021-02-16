from django.urls import path
from . import views

app_name = "learning_path"

urlpatterns = [
    path("learning-path/", views.LearningPathView.as_view(), name="paths"),
]