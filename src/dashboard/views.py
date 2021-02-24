from django.contrib.auth.decorators import login_required
from django.db.models.aggregates import Count, Sum
from django.utils.decorators import method_decorator
from django.views.generic.edit import CreateView
from blog.forms import CreatePostForm
from blog.models import Post
from users.decorators import staff_required, teacher_required
from django.views.generic import View, ListView
from django.shortcuts import redirect, render
from course.models import Course
from userlogs.models import UserLog
from users.models import CustomUser
from course.forms import CreateCourse


@login_required
def dashboard_view(request):
    user = request.user
    if user.is_student:
        pass  # student dashboard
    if user.is_teacher and user.is_staff:
        return redirect("dashboard:staff")
    if user.is_teacher:
        return redirect("dashboard:instructor")


@method_decorator([staff_required], name="dispatch")
class StaffView(View):
    template_name = "staff/dashboard.html"

    def get(self, request, *args, **kwargs):
        total_courses = Course.objects.count()
        total_users = CustomUser.objects.count()
        total_students = CustomUser.objects.filter(is_student=True).count()
        logs = UserLog.objects.all()[:10]

        context = {
            "title": "Staff",
            "total_courses": total_courses,
            "total_users": total_users,
            "total_students": total_students,
            "logs": logs,
        }
        return render(request, self.template_name, context)


class UserLogList(ListView):
    model = UserLog
    context_object_name = "logs"


@method_decorator([teacher_required], name="dispatch")
class InstructorView(View):
    template_name = "instructor/dashboard.html"

    def get(self, request, *args, **kwargs):
        instructor = request.user
        courses_published = Course.objects.filter(teacher=instructor, published=True)
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


@method_decorator([teacher_required], name="dispatch")
class CourseListView(ListView):
    paginate_by = 10

    def get(self, request, *args, **kwargs):
        user = self.request.user
        courses = []
        if user.is_teacher:
            courses = Course.objects.filter(teacher=user).order_by("-date_created")
            template_name = "instructor/courses.html"
        if user.is_student:
            courses = Course.objects.filter(students__id__exact=user.id).order_by(
                "-date_created"
            )
            template_name = "student/courses.html"

        context = {"courses": courses}
        return render(request, template_name, context)


@method_decorator([teacher_required], name="dispatch")
class TutorialListView(ListView):
    template_name = "instructor/tutorials.html"
    paginate_by = 10

    def get(self, request, *args, **kwargs):
        user = self.request.user
        tutorials = Post.objects.filter(author=user).order_by("-publish_date")
        context = {"tutorials": tutorials}
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
