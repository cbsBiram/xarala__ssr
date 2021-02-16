from django.views.generic import TemplateView

# Create your views here.
class LearningPathView(TemplateView):
    template_name = "learning_path.html"