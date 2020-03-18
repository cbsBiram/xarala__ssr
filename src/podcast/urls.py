from django.urls import path
from .views import EpisodeListView

urlpatterns = [
    path("", EpisodeListView.as_view(), name="episodes")
]
