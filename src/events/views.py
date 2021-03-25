from django.views.generic import ListView, DetailView
from .models import Event


class EventListView(ListView):
    model = Event
    queryset = Event.objects.published()
    context_object_name = "events"
    paginate_by = 4
    template_name = "event-list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class EventDetailView(DetailView):
    model = Event
    template_name = "event-details.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
