from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from .models import Course, Chapter, Lesson


class CourseListView(ListView):
    model = Course
    context_object_name = 'courses'


class CourseOverviewView(DetailView):
    model = Course
    template_name = "course/course_overview.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class CourseDetailView(DetailView):
    model = Course
    template_name = "course/course_detail.html"

    def get_context_data(self, **kwargs):
        lesson = Lesson.objects.get(slug=self.request.GET.get('lecture'))
        context = super().get_context_data(**kwargs)
        context['lesson'] = lesson
        return context
