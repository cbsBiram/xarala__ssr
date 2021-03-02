from django.contrib.auth.decorators import login_required
from django.db.models.aggregates import Count, Sum
from django.http.response import JsonResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from users.decorators import teacher_required
from django.views.generic import View, ListView
from django.shortcuts import get_object_or_404, redirect, render
from course.models import Chapter, Course
from userlogs.models import UserLog
from course.forms import CreateChapter, CreateCourse, UpdateChapter, UpdateCourse


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
        form_update = self.form_class_update()
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
def publish_course(request):
    user = request.user
    values = {"error": "", "has_error": 0}
    course_id = int(request.POST.get("id"))
    try:
        course = Course.objects.get(pk=course_id, teacher=user)
        if not course.submitted and not course.published:
            course.submitted = True
        elif course.submitted:
            course.published = True
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


@teacher_required
def create_chapter(request, slug):
    # template_name = "instructor/manage-course.html"
    form_class = CreateChapter
    form = form_class(request.POST)
    values = {"error": "", "has_error": 0}
    course = Course.objects.get(slug=slug)
    if form.is_valid():
        chapter = form.save(commit=False)
        chapter.course = course
        chapter.save()
        course.course_chapters.add(chapter)
    return JsonResponse(values)


@teacher_required
def update_chapter(request, slug):
    # template_name = "instructor/manage-course.html"
    instance = get_object_or_404(Chapter, slug=slug)
    form_class = CreateChapter
    form = form_class(request.POST, instance=instance)
    values = {"error": "", "has_error": 0}
    if form.is_valid():
        form.save()
    return JsonResponse(values)


# @teacher_required
# def delete_chapter(request, slug):
#     # template_name = "instructor/manage-course.html"
#     instance = get_object_or_404(Chapter, slug=slug)
#     form_class = CreateChapter
#     form = form_class(request.POST, instance=instance)
#     values = {"error": "", "has_error": 0}
#     if form.is_valid():
#         form.save()
#     return JsonResponse(values)
