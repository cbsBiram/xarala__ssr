from django.http import JsonResponse
from django.core import serializers
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from .models import Course, Chapter, Lesson, CustomUser


class CourseListView(ListView):
    queryset = Course.objects.order_by('-date_created')
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


def subscribe_user_to_course(request):
    values = {'error': '', 'has_error': 0}
    user_id = request.POST.get('user_id')
    course_id = request.POST.get('course_id')
    try:
        user = CustomUser.objects.get(pk=int(user_id))
        course = Course.objects.get(pk=int(course_id))
        course.users.add(user)
        return JsonResponse(values)
    except Exception as e:
        print("Error ", e)
        return JsonResponse(values)
