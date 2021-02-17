from django.views.generic import ListView, DetailView, TemplateView
from .models import Episode


class EpisodeListView(ListView):
    model = Episode
    context_object_name = "episods"
    template_name = "episode_list.html"


class EpisodeDetail(DetailView):
    model = Episode
    template_name = "episode_detail.html"


class HowWePodcast(TemplateView):
    template_name = "how-we-podcast.html"
