from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Episode


class EpisodeListView(ListView):
    model = Episode
    context_object_name = 'episods'
    # template_name=''


class EpisodeDetail(DetailView):
    model = Episode
    # template_name=''
