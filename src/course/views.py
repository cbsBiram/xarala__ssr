from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.core import serializers
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView
from .models import Course, Chapter, Lesson, CustomUser


class CourseListView(ListView):
    queryset = Course.objects.order_by('-date_created')
    context_object_name = 'courses'


class CourseOverviewView(DetailView):
    model = Course
    template_name = "course/course_overview.html"

    def get_context_data(self, **kwargs):
        student = self.request.user
        context = super().get_context_data(**kwargs)
        button_text = "Voir la formation"
        if student.is_authenticated and context.get("course") in student.courses_enrolled.all():
            pass
        else:
            button_text = "S'inscrire"
        context['button_text'] = button_text
        return context


class CourseDetailView(DetailView):
    model = Course
    template_name = "course/course_detail.html"

    def get_context_data(self, **kwargs):
        lesson = Lesson.objects.get(slug=self.request.GET.get('lecture'))
        context = super().get_context_data(**kwargs)
        context['lesson'] = lesson
        return context


@login_required(login_url="login")
def subscribe_user_to_course(request, course_slug):
    values = {'error': '', 'has_error': 0}
    course = get_object_or_404(Course, slug=course_slug)
    student = request.user
    try:
        if student.is_authenticated:
            if course not in student.courses_enrolled.all():
                student.courses_enrolled.add(course)
                messages.success(
                    request, "Vous êtes inscrit avec succes...")
                return redirect(f"/courses/{course.slug}/overview")
            else:
                return redirect(f"/courses/{course.slug}/overview")
    except Exception as e:
        print("Error ", e)
        return JsonResponse(values)


class UserCourseListView(ListView):
    def get_queryset(self):
        student = self.request.user
        return student.courses_enrolled.all()
    context_object_name = 'courses'
