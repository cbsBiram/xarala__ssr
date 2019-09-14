from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Course, Lesson


class CourseListView(ListView):
    model = Course
    context_object_name = 'courses'


class CourseDetailView(DetailView):
    model = Course
    # template_name = "courselist.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['now'] = timezone.now()
        return context


class LessonDetailView(DetailView):
    model = Lesson

    def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            # context['now'] = timezone.now()
            return context
