from django.views.generic import TemplateView, DetailView
from .models import LearningPath


class LearningPathView(TemplateView):
    template_name = "learning_path.html"
    queryset = LearningPath.objects.published()
    paginate_by = 2
    context_object_name = "learning_paths"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class LearningPathDetailView(DetailView):
    model = LearningPath
    template_name = "learning_path_details.html"
    context_object_name = "learning_path"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
