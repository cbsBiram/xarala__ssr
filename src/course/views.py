from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils.decorators import method_decorator
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy
from users.decorators import teacher_required, student_required
from django.contrib import messages
from django.http import JsonResponse, HttpResponseRedirect
from django.core import serializers
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, View, TemplateView
from .models import Course, Chapter, Lesson, Category
from .forms import CreateCourse, CreateChapter, CreateLesson
from userlogs.models import UserLog


class CourseListView(ListView):
    queryset = Course.objects.order_by("-id")
    paginate_by = 4
    context_object_name = "courses"


class CourseOverviewView(DetailView):
    model = Course
    template_name = "course/course_overview.html"

    def get_context_data(self, **kwargs):
        student = self.request.user
        context = super().get_context_data(**kwargs)
        button_text = "Commencer"
        if (
            student.is_authenticated
            and context.get("course") in student.courses_enrolled.all()
        ):
            pass
        else:
            button_text = "Enroller"
        context["button_text"] = button_text
        return context


@method_decorator([login_required], name="dispatch")
class CourseDetailView(DetailView):
    model = Course
    template_name = "course/course_detail.html"

    def get_context_data(self, **kwargs):
        slug = self.request.GET.get("lecture")
        lesson = Lesson.objects.get(slug=slug)
        context = super().get_context_data(**kwargs)
        context["lesson"] = lesson
        return context


@login_required(login_url="login")
def subscribe_user_to_course(request, course_slug):
    values = {"error": "", "has_error": 0}
    course = get_object_or_404(Course, slug=course_slug)
    student = request.user
    try:
        if student.is_authenticated:
            if course not in student.courses_enrolled.all():
                student.courses_enrolled.add(course)
                UserLog.objects.create(
                    action=f"Enrolled {course} course",
                    user_type="Student",
                    user=student,
                )
                messages.success(request, "Formation enrollée...")
                return redirect(f"/courses/{course.slug}/overview")
            else:
                return redirect(f"/courses/{course.slug}/overview")
    except Exception as e:
        print("Error ", e)
        return JsonResponse(values)


@method_decorator([student_required], name="dispatch")
class StudentCourseListView(ListView):
    def get_queryset(self):
        student = self.request.user
        return student.courses_enrolled.all()

    context_object_name = "courses"


@method_decorator([teacher_required], name="dispatch")
class TeacherCourseListView(ListView, CreateView):
    form_class = CreateCourse
    template_name = "dashboard/teacher/course-admin.html"

    def get(self, request, *args, **kwargs):
        teacher = self.request.user
        courses = teacher.courses_created.all()
        form = self.form_class()
        title = "Vos Formations"
        return render(
            request,
            self.template_name,
            {"form": form, "courses": courses, "title": title},
        )

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        teacher = self.request.user
        if form.is_valid():
            title = form.cleaned_data.get("title")
            level = form.cleaned_data.get("level")
            language = form.cleaned_data.get("language")
            published = form.cleaned_data.get("published")
            description = form.cleaned_data.get("description")
            thumbnail = form.cleaned_data.get("thumbnail")
            course = Course(
                title=title,
                level=level,
                language=language,
                description=description,
                published=published,
                thumbnail=thumbnail,
                teacher=teacher,
            )
            course.save()
            UserLog.objects.create(
                action=f"Created {title} course", user_type="Instructeur", user=teacher
            )
            return redirect("created-courses")

        return render(request, self.template_name, {"form": form})


class TeacherChapterListCreateView(DetailView, CreateView):
    form_class = CreateChapter
    template_name = "dashboard/teacher/add-chapter.html"

    def get(self, request, *args, **kwargs):
        teacher = self.request.user
        course_id = request.GET.get("course_id")
        course = Course.objects.get(pk=int(course_id))
        chapters = course.course_chapters.all()
        form = self.form_class()
        return render(request, self.template_name, {"form": form, "chapters": chapters})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        teacher = self.request.user
        if form.is_valid():
            name = form.cleaned_data.get("name")
            course_id = request.GET.get("course_id")
            chapter = Chapter(name=name)
            chapter.save()
            course = Course.objects.get(pk=int(course_id))
            course.course_chapters.add(chapter)
            return redirect(f"/dashboard/teacher/{course.slug}/?course_id={course_id}")

        return render(request, self.template_name, {"form": form})


@method_decorator([teacher_required], name="dispatch")
class TeacherLessonListCreateView(DetailView, CreateView):
    form_class = CreateLesson
    template_name = "dashboard/teacher/add-lesson.html"

    def get(self, request, *args, **kwargs):
        teacher = self.request.user
        chapter_id = request.GET.get("chapter_id")
        chapter = Chapter.objects.get(pk=int(chapter_id))
        lessons = chapter.course_lessons.all()
        form = self.form_class()
        return render(request, self.template_name, {"form": form, "lessons": lessons})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        teacher = self.request.user
        if form.is_valid():
            title = form.cleaned_data.get("title")
            video_link = form.cleaned_data.get("video_id")
            if "www.youtube.com/" or "https://youtu.be/" in video_link:
                video_id = video_link[-11:]
            else:
                video_id = form.cleaned_data.get("video_id")
            text = form.cleaned_data.get("text")
            platform = form.cleaned_data.get("platform")
            chapter_id = request.GET.get("chapter_id")
            lesson = Lesson(
                title=title, video_id=video_id, text=text, platform=platform
            )
            lesson.save()
            chapter = Chapter.objects.get(pk=int(chapter_id))
            chapter.course_lessons.add(lesson)
            return redirect(
                f"/dashboard/teacher/{chapter.slug}/lesson/?chapter_id={chapter_id}"
            )

        return render(request, self.template_name, {"form": form})


# categories


class CategoryCourseList(ListView):

    template_name = "course/courses_by_category.html"

    def get_queryset(self):
        self.category = get_object_or_404(Category, name=self.kwargs["category"])
        return Course.objects.filter(categories=self.category)

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in the publisher
        context["category"] = self.category
        return context


class LearningPathView(TemplateView):
    template_name = "course/learning_path.html"


class ProfessionalTrainingView(TemplateView):
    template_name = "course/professional_training.html"
