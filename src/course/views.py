from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.http import JsonResponse, HttpResponseRedirect
from django.core import serializers
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView
from .models import Course, Chapter, Lesson, CustomUser
from .forms import CreateCourse


def profile_check(user):
    return user.user_type('TC')


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
        slug = self.request.GET.get('lecture')
        lesson = Lesson.objects.get(slug=slug)
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


class StudentCourseListView(ListView):
    def get_queryset(self):
        student = self.request.user
        return student.courses_enrolled.all()
    context_object_name = 'courses'


# @method_decorator(login_required, name='dispatch')
class TeacherCourseListView(ListView, CreateView):
    form_class = CreateCourse
    template_name = "dashboard/teacher/course-admin.html"

    def get(self, request, *args, **kwargs):
        teacher = self.request.user
        courses = teacher.courses_created.all()
        form = self.form_class()
        return render(request, self.template_name, {'form': form, 'courses': courses})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        teacher = self.request.user
        if form.is_valid():
            title = form.cleaned_data.get('title')
            level = form.cleaned_data.get('level')
            language = form.cleaned_data.get('language')
            published = form.cleaned_data.get('published')
            description = form.cleaned_data.get('description')
            thumbnail = form.cleaned_data.get('thumbnail')
            course = Course(title=title,
                            level=level,
                            language=language,
                            description=description,
                            published=published,
                            thumbnail=thumbnail,
                            teacher=teacher)
            course.save()
            return redirect('/courses/dashboard/teacher/')

        return render(request, self.template_name, {'form': form})


# class TeacherChapterListCreateView(ListView, CreateView):
#     form_class = CreateCourse
#     template_name = "dashboard/teacher/course-admin.html"

#     def get(self, request, *args, **kwargs):
#         teacher = self.request.user
#         courses = teacher.courses_created.all()
#         form = self.form_class()
#         return render(request, self.template_name, {'form': form, 'courses': courses})

#     def post(self, request, *args, **kwargs):
#         form = self.form_class(request.POST)
#         teacher = self.request.user
#         if form.is_valid():
#             title = form.cleaned_data.get('title')
#             level = form.cleaned_data.get('level')
#             language = form.cleaned_data.get('language')
#             published = form.cleaned_data.get('published')
#             course = Course(title=title,
#                             level=level,
#                             language=language,
#                             published=published,
#                             teacher=teacher)
#             course.save()
#             return redirect('/courses/dashboard/teacher/')

#         return render(request, self.template_name, {'form': form})
