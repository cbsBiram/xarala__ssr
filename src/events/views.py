from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Event


class EventListView(ListView):
    model = Event
    context_object_name = "events"
    paginate_by = 4

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class EventDetailView(DetailView):
    model = Event

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
