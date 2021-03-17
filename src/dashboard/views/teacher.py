from django.contrib.auth.decorators import login_required
from django.db.models.aggregates import Count, Sum
from django.http.response import JsonResponse
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.generic.edit import CreateView, UpdateView
from quiz.models import Quiz
from users.decorators import teacher_required
from django.views.generic import View, ListView
from django.shortcuts import get_object_or_404, redirect, render
from course.models import Category, Chapter, Course, Language, Lesson
from userlogs.models import UserLog
from course.forms import (
    CreateChapter,
    CreateCourse,
    CreateLesson,
    CreateQuiz,
    LEVEL,
    UpdateLesson,
    UpdateChapter,
    UpdateCourse,
)
from xarala.utils import format_date
from json import loads as jsonloads


@method_decorator([teacher_required], name="dispatch")
class InstructorView(View):
    template_name = "instructor/dashboard.html"

    def get(self, request, *args, **kwargs):
        instructor = request.user
        courses_published = Course.objects.filter(teacher=instructor, published=True)[
            :10
        ]
        total_sales = courses_published.aggregate(Sum("price"))["price__sum"]
        total_enroll = courses_published.aggregate(Count("students"))["students__count"]
        courses_unpublished = Course.objects.filter(teacher=instructor, published=False)

        context = {
            "total_sales": total_sales,
            "total_enroll": total_enroll,
            "courses_published": courses_published,
            "courses_unpublished": courses_unpublished,
        }

        return render(request, self.template_name, context)


@method_decorator([login_required], name="dispatch")
class CourseListView(ListView):
    template_name = "courses.html"
    paginate_by = 10

    def get(self, request, *args, **kwargs):
        user = self.request.user
        courses = None
        if user.is_teacher:
            courses = Course.objects.filter(teacher=user).order_by("-date_created")
        if user.is_student:
            courses = Course.objects.filter(students__id__exact=user.id).order_by(
                "-date_created"
            )

        context = {"courses": courses, "user": user}
        return render(request, self.template_name, context)


# @method_decorator([teacher_required], name="dispatch")
# class CourseCreateView(CreateView):
#     form_class = CreateCourse
#     template_name = "instructor/create-course.html"

#     def post(self, request, *args, **kwargs):
#         form = self.form_class(request.POST, request.FILES)
#         teacher = self.request.user
#         if form.is_valid():
#             course = form.save(commit=False)
#             course.teacher = teacher
#             course.save()
#             form.save_m2m()
#             UserLog.objects.create(
#                 action=f"Created {course.title} course",
#                 user_type="Instructeur",
#                 user=teacher,
#             )
#             return redirect("dashboard:courses")

#         return render(request, self.template_name, {"form": form})


@method_decorator([teacher_required], name="dispatch")
class CourseCreateView(CreateView):
    form_class = CreateCourse
    template_name = "instructor/create-course.html"

    def get(self, request, *args, **kwargs):
        languages = Language.objects.all()
        levels = LEVEL
        categories = Category.objects.all()

        context = {
            "levels": levels,
            "languages": languages,
            "categories": categories,
        }
        return render(request, self.template_name, context=context)

    def post(self, request, *args, **kwargs):
        user = request.user
        if request.POST:
            values = {"error": "", "has_error": 0}
            try:
                course_title = request.POST.get("courseTitle", "")
                chapters = jsonloads(request.POST.get("chapters", ""))
                lessons = jsonloads(request.POST.get("lessons", ""))

                course = Course.objects.create(title=course_title, teacher=user)
                UserLog.objects.create(
                    action=f"Created {course.title} course",
                    user_type="Instructeur",
                    user=user,
                )
                for chapter in chapters:
                    Chapter.objects.create(name=chapter.get("chapter"), course=course)
                for lesson in lessons:
                    chapter = Chapter.objects.get(name=lesson.get("chapter"))
                    Lesson.objects.create(
                        title=lesson.get("title", ""),
                        video_id=lesson.get("videoId", ""),
                        chapter=chapter,
                        text=lesson.get("text", ""),
                    )
                values["id"] = course.id
                values["title"] = course.title
            except Exception as e:
                values["error"] = e
                values["has_error"] = -1
            return JsonResponse(values)

        return render(request, self.template_name)


@teacher_required
def submit_course(request):
    user = request.user
    if request.POST:
        course_id = request.POST.get("id")
        course = Course.objects.get(pk=course_id, teacher=user)
        language = Language.objects.get(name=request.POST.get("language", ""))
        course.submitted = True
        course.description = request.POST.get("description", "")
        course.level = request.POST.get("level", "")
        course.language = language
        course.thumbnail = request.POST.get("thumbnail", "")
        course.level = request.POST.get("level", "")
        course.save()
        return redirect("dashboard:courses")
    return JsonResponse({})


@method_decorator([teacher_required], name="dispatch")
class CourseUpdateView(UpdateView):
    model = Course
    form_class = UpdateCourse
    template_name = "instructor/edit-course.html"


# @teacher_required
# def submit_course(request):
#     user = request.user
#     values = {"error": "", "has_error": 0}
#     course_id = int(request.POST.get("id"))
#     try:
#         course = Course.objects.get(pk=course_id, teacher=user)
#         if not course.submitted:
#             course.submitted = True
#         else:
#             if not course.published:
#                 course.published = True
#         course.save()
#     except Exception as e:
#         values["error"] = e
#         values["has_error"] = -1
#     return JsonResponse(values)


@teacher_required
def draft_course(request):
    user = request.user
    values = {"error": "", "has_error": 0}
    course_id = int(request.POST.get("id"))
    try:
        course = Course.objects.get(pk=course_id, teacher=user)
        course.drafted = True
        course.save()
    except Exception as e:
        values["error"] = e
        values["has_error"] = -1
    return JsonResponse(values)


@method_decorator([teacher_required], name="dispatch")
class CourseManagementView(View):
    template_name = "instructor/_manage-course.html"
    form_class = CreateChapter
    form_class_update = UpdateChapter
    form_class_quiz = CreateQuiz
    paginate_by = 10

    def get(self, request, *args, **kwargs):
        course = Course.objects.get(slug=self.kwargs["slug"])
        form = self.form_class()
        form_update = self.form_class_update(auto_id="update_%s")
        form_quiz = self.form_class_quiz(auto_id="quiz_%s")
        context = {
            "chapters": course.get_chapters(),
            "course": course,
            "form": form,
            "form_update": form_update,
            "form_quiz": form_quiz,
        }

        return render(request, self.template_name, context=context)


@teacher_required
def create_chapter(request, slug):
    form_class = CreateChapter
    form = form_class(request.POST)
    values = {"error": "", "has_error": 0}
    try:
        course = Course.objects.get(slug=slug)
        if form.is_valid():
            chapter = form.save(commit=False)
            chapter.course = course
            chapter.save()
            values["id"] = chapter.id
            values["name"] = chapter.name
            values["chapter_slug"] = chapter.slug
            values["date_created"] = format_date(chapter.date_created)
            values["order"] = chapter.order
            values["drafted"] = "Oui" if chapter.drafted else "Non"
            course.course_chapters.add(chapter)
            print(values)
    except Exception as e:
        values["error"] = e
        values["has_error"] = -1
    return JsonResponse(values)


@teacher_required
def update_chapter(request, id):
    values = {"error": "", "has_error": 0}
    name = request.POST.get("name")
    try:
        chapter = get_object_or_404(Chapter, id=id)
        chapter.name = name
        chapter.save()
        values["id"] = chapter.id
        values["name"] = chapter.name
        values["chapter_slug"] = chapter.slug
        values["date_created"] = format_date(chapter.date_created)
        values["order"] = chapter.order
        values["drafted"] = "Oui" if chapter.drafted else "Non"
    except Exception as e:
        values["error"] = e
        values["has_error"] = -1
    return JsonResponse(values)


@teacher_required
def delete_chapter(request, id):
    values = {"error": "", "has_error": 0}
    try:
        chapter = get_object_or_404(Chapter, id=id)
        if request.method == "POST":
            chapter.delete()
    except Exception as e:
        values["error"] = e
        values["has_error"] = -1
    return JsonResponse(values)


@teacher_required
def draft_chapter(request, id):
    values = {"error": "", "has_error": 0}
    try:
        chapter = get_object_or_404(Chapter, id=id)
        chapter.drafted = True
        chapter.save()
        values["chapter_slug"] = chapter.slug
    except Exception as e:
        values["error"] = e
        values["has_error"] = -1
    return JsonResponse(values)


class ChapterManagementView(View):
    template_name = "instructor/manage-chapter.html"
    form_class = CreateLesson
    form_class_update = UpdateLesson
    paginate_by = 10

    def get(self, request, *args, **kwargs):
        chapter = Chapter.objects.get(slug=self.kwargs["slug"])
        form = self.form_class()
        form_update = self.form_class_update(auto_id="update_%s")
        return render(
            request,
            self.template_name,
            {
                "lessons": chapter.course_lessons.all(),
                "chapter": chapter,
                "form": form,
                "form_update": form_update,
            },
        )


@method_decorator([teacher_required], name="dispatch")
class LessonCreateView(CreateView):
    form_class = CreateLesson
    template_name = "instructor/create-lesson.html"

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        chapter = Chapter.objects.get(slug=self.kwargs["slug"])
        if form.is_valid():
            lesson = form.save(commit=False)
            lesson.chapter = chapter
            lesson.save()
            chapter.course_lessons.add(lesson)
            return redirect(
                reverse("dashboard:manage-course", args=[chapter.course.slug])
            )

        return render(request, self.template_name, {"form": form})


@teacher_required
def update_lesson(request, id):
    instance = Lesson.objects.get(id=id)
    form_class = UpdateLesson
    form = form_class(request.POST or None, instance=instance)
    if form.is_valid():
        lesson = form.save(commit=False)
        lesson.save()
        return redirect(
            reverse("dashboard:manage-course", args=[lesson.chapter.course.slug])
        )

    template_name = "instructor/edit-lesson.html"
    return render(request, template_name, {"form": form, "lesson": instance})


@teacher_required
def create_quiz(request, slug):
    teacher = request.user
    form_class = CreateQuiz
    form = form_class(request.POST)
    values = {"error": "", "has_error": 0}
    try:
        chapter = Chapter.objects.get(slug=slug)
        print(form.errors)
        if form.is_valid():
            quiz = form.save(commit=False)
            quiz.chapter = chapter
            quiz.save()
            values["chapter_id"] = chapter.id
            values["chapter_slug"] = chapter.slug
            values["quiz_id"] = quiz.id
            values["title"] = quiz.title
            values["description"] = quiz.description
            UserLog.objects.create(
                action=f"Created {quiz.title} quiz",
                user_type="Instructeur",
                user=teacher,
            )
    except Exception as e:
        values["error"] = e
        values["has_error"] = -1
    return JsonResponse(values)


@teacher_required
def update_quiz(request, slug):
    instance = Quiz.objects.get(chapter__slug=slug)
    form_class = CreateQuiz
    form = form_class(request.POST or None, instance=instance)
    if form.is_valid():
        quiz = form.save(commit=False)
        quiz.save()
        return redirect(
            reverse("dashboard:manage-course", args=[quiz.chapter.course.slug])
        )

    template_name = "instructor/edit-quiz.html"
    context = {"form": form, "quiz": instance}
    return render(request, template_name, context=context)


@teacher_required
def delete_quiz(request, slug):
    values = {"error": "", "has_error": 0}
    try:
        quiz = get_object_or_404(Quiz, chapter__slug=slug)
        if request.method == "POST":
            quiz.delete()
    except Exception as e:
        values["error"] = e
        values["has_error"] = -1
    return JsonResponse(values)
