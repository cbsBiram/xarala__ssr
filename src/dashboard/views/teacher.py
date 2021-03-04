from django.contrib.auth.decorators import login_required
from django.db.models.aggregates import Count, Sum
from django.http.response import JsonResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from users.decorators import teacher_required
from django.views.generic import View, ListView
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from course.models import Chapter, Course, Lesson
from userlogs.models import UserLog
from course.forms import (
    CreateChapter,
    CreateCourse,
    CreateLesson,
    UpdateLesson,
    UpdateChapter,
    UpdateCourse,
)


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


@method_decorator([teacher_required], name="dispatch")
class CourseCreateView(CreateView):
    form_class = CreateCourse
    template_name = "instructor/create-course.html"

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        teacher = self.request.user
        if form.is_valid():
            course = form.save(commit=False)
            course.teacher = teacher
            course.save()
            form.save_m2m()
            UserLog.objects.create(
                action=f"Created {course.title} course",
                user_type="Instructeur",
                user=teacher,
            )
            return redirect("dashboard:courses")

        return render(request, self.template_name, {"form": form})


@method_decorator([teacher_required], name="dispatch")
class CourseUpdateView(UpdateView):
    model = Course
    form_class = UpdateCourse
    template_name = "instructor/edit-course.html"


@teacher_required
def submit_course(request):
    user = request.user
    values = {"error": "", "has_error": 0}
    course_id = int(request.POST.get("id"))
    try:
        course = Course.objects.get(pk=course_id, teacher=user)
        course.submitted = True
        course.save()
    except Exception as e:
        values["error"] = e
        values["has_error"] = -1
        print(e)
    return JsonResponse(values)


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
        print(e)
    return JsonResponse(values)


@method_decorator([teacher_required], name="dispatch")
class CourseDeleteView(DeleteView):
    model = Course
    success_url = reverse_lazy("dashboard:courses")


@method_decorator([teacher_required], name="dispatch")
class CourseManagementView(View):
    template_name = "instructor/manage-course.html"
    form_class = CreateChapter
    form_class_update = UpdateChapter
    paginate_by = 10

    def get(self, request, *args, **kwargs):
        course = Course.objects.get(slug=self.kwargs["slug"])
        form = self.form_class()
        form_update = self.form_class_update(auto_id="update_%s")
        return render(
            request,
            self.template_name,
            {
                "chapters": course.get_chapters(),
                "course": course,
                "form": form,
                "form_update": form_update,
            },
        )


@teacher_required
def create_chapter(request, slug):
    form_class = CreateChapter
    form = form_class(request.POST)
    print(request.POST.get("name"))
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
            values["date_created"] = chapter.date_created
            values["order"] = chapter.order
            values["drafted"] = "Oui" if chapter.drafted else "Non"
            values["course_slug"] = slug
            values["course_id"] = course.id
            course.course_chapters.add(chapter)
            messages.success(request, "Chapitre ajouté avec succès!")
            print(values)
    except Exception as e:
        values["error"] = e
        values["has_error"] = -1
    return JsonResponse(values)


@teacher_required
def update_chapter(request, id):
    values = {"error": "", "has_error": 0}
    try:
        instance = get_object_or_404(Chapter, id=id)
        print(id)
        print(instance)
        form_class = CreateChapter
        form = form_class(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            messages.success(request, "Chapitre modifié avec succès!")
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
            messages.success(request, "Chapitre Supprimé avec succès.")
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
                "lessons": chapter.course_lessons,
                "chapter": chapter,
                "form": form,
                "form_update": form_update,
            },
        )


@teacher_required
def create_lesson(request, slug):
    form_class = CreateLesson
    form = form_class(request.POST)
    values = {"error": "", "has_error": 0}
    try:
        chapter = Chapter.objects.get(slug=slug)
        if form.is_valid():
            lesson = form.save(commit=False)
            lesson.chapter = chapter
            lesson.save()
            values["id"] = lesson.id
            values["title"] = lesson.name
            values["lesson_slug"] = lesson.slug
            values["date_created"] = lesson.date_created
            values["order"] = lesson.order
            values["drafted"] = "Oui" if lesson.drafted else "Non"
            values["chapter_slug"] = slug
            values["chapter_id"] = chapter.id
            chapter.course_lessons.add(lesson)
            messages.success(request, "Leçon ajoutée avec succès!")
    except Exception as e:
        values["error"] = e
        values["has_error"] = -1
    return JsonResponse(values)


@teacher_required
def update_lesson(request, id):
    values = {"error": "", "has_error": 0}
    try:
        instance = get_object_or_404(Lesson, id=id)
        form_class = CreateLesson
        form = form_class(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            messages.success(request, "Leçon modifiée avec succès!")
    except Exception as e:
        values["error"] = e
        values["has_error"] = -1
    return JsonResponse(values)


@teacher_required
def delete_lesson(request, id):
    values = {"error": "", "has_error": 0}
    try:
        lesson = get_object_or_404(Lesson, id=id)
        if request.method == "POST":
            lesson.delete()
            messages.success(request, "Leçon Supprimée avec succès.")
    except Exception as e:
        values["error"] = e
        values["has_error"] = -1
    return JsonResponse(values)
