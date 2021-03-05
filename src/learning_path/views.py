from django.views.generic import TemplateView, DetailView
from .models import LearningPath

# Create your views here.
class LearningPathView(TemplateView):
    template_name = "learning_path.html"
    queryset = LearningPath.objects.all()
    paginate_by = 2
    context_object_name = "learning_path"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["learning_path"] = LearningPath.objects.all()
        return context


class ShowLearningPathView(DetailView):
    model = LearningPath
    template_name = "show_learning_path.html"

    def get_context_data(self, **kwargs):
        # title = self.request.GET.get("title")
        # learning_path = LearningPath.objects.get(title=title)
        context = super().get_context_data(**kwargs)
        context["learning_path"] = LearningPath.objects.all()
        return context

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()
        title = self.kwargs.get("title") or self.request.GET.get("title") or None
        queryset = queryset.filter(title=title)
        obj = queryset.get()
        return obj
