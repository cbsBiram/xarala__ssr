from django.urls import path
from .views import EpisodeListView, EpisodeDetail, HowWePodcast

app_name = "podcast"

urlpatterns = [
    path("", EpisodeListView.as_view(), name="episodes"),
    path("details/<int:id>/", EpisodeDetail.as_view(), name="episodes-detail"),
    path("how-we-podcast/", HowWePodcast.as_view(), name="how-we-podcast"),
]
