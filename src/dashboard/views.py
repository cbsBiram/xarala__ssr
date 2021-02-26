from django.contrib.auth.decorators import login_required
from django.db.models.aggregates import Count, Sum
from django.http.response import JsonResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from blog.forms import CreatePostForm, UpdatePostForm
from blog.models import Post
from users.decorators import staff_required, student_required, teacher_required
from django.views.generic import View, ListView
from django.shortcuts import redirect, render
from course.models import Course
from userlogs.models import UserLog
from users.models import CustomUser
from course.forms import CreateCourse, UpdateCourse


@login_required
def dashboard_view(request):
    user = request.user
    if user.is_student:
        return redirect("dashboard:student")
    if user.is_teacher and user.is_staff:
        return redirect("dashboard:staff")
    if user.is_teacher:
        return redirect("dashboard:instructor")
    else:
        return redirect("oauth-new-password")


class UserLogList(ListView):
    model = UserLog
    context_object_name = "logs"


@method_decorator([staff_required], name="dispatch")
class StaffView(View):
    template_name = "staff/dashboard.html"

    def get(self, request, *args, **kwargs):
        total_courses = Course.objects.count()
        total_teachers = CustomUser.objects.filter(is_teacher=True).count()
        total_students = CustomUser.objects.filter(is_student=True).count()
        logs = UserLog.objects.all()[:10]

        context = {
            "title": "Staff",
            "total_courses": total_courses,
            "total_teachers": total_teachers,
            "total_students": total_students,
            "logs": logs,
        }
        return render(request, self.template_name, context)


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


@method_decorator([student_required], name="dispatch")
class StudentView(View):
    template_name = "student/dashboard.html"

    def get(self, request, *args, **kwargs):
        student = request.user
        courses_purchased = Course.objects.filter(students__id__exact=student.id)
        total_instructor_subscribing = (
            courses_purchased.order_by("teacher").distinct("teacher").count()
        )

        context = {
            "courses": courses_purchased,
            "total_instructor_subscribing": total_instructor_subscribing,
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


@method_decorator([login_required], name="dispatch")
class TutorialListView(ListView):
    template_name = "tutorials.html"
    paginate_by = 10

    def get(self, request, *args, **kwargs):
        user = self.request.user
        tutorials = Post.objects.filter(author=user).order_by("-publish_date")
        context = {"tutorials": tutorials, "user": user}
        return render(request, self.template_name, context)


@method_decorator([login_required], name="dispatch")
class TutorialCreateView(CreateView):
    form_class = CreatePostForm
    template_name = "instructor/create-tutorial.html"

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        user = self.request.user
        if form.is_valid():
            post = form.save(commit=False)
            post.author = user
            post.save()
            UserLog.objects.create(
                action=f"Created {post.title} post", user_type="Writer", user=user
            )
            return redirect("dashboard:tutorials")

        return render(request, self.template_name, {"form": form})


@method_decorator([login_required], name="dispatch")
class TutorialDeleteView(DeleteView):
    model = Post
    success_url = reverse_lazy("dashboard:tutorials")


@method_decorator([login_required], name="dispatch")
class TutorialUpdateView(UpdateView):
    model = Post
    form_class = UpdatePostForm
    template_name = "instructor/edit-tutorial.html"


@login_required
def publish_tutorial(request):
    user = request.user
    values = {"error": "", "has_error": 0}
    tutorial_id = int(request.POST.get("id"))
    try:
        tutorial = Post.objects.get(pk=tutorial_id, author=user)
        if not tutorial.submitted and not tutorial.published:
            tutorial.submitted = True
        elif tutorial.submitted:
            tutorial.published = True
        tutorial.save()
    except Exception as e:
        values["error"] = e
        values["has_error"] = -1
        print(e)
    return JsonResponse(values)
