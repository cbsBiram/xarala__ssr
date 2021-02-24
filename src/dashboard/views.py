from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models.aggregates import Count, Sum
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic.edit import CreateView, DeleteView
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
        return redirect("dashboard:instructor-dashboard")


@method_decorator([staff_required], name="dispatch")
class StaffView(View):
    template_name = "staff/dashboard.html"

    def get(self, request, *args, **kwargs):
        total_courses = Course.objects.count()
        total_users = CustomUser.objects.count()
        total_students = CustomUser.objects.filter(is_student=True).count()
        logs = UserLog.objects.all()[:3]

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
    def get(self, request, *args, **kwargs):
        user = self.request.user
        page = request.GET.get("page", 1)

        if user.is_teacher:
            course_list = Course.objects.filter(teacher=user).order_by("-date_created")
            template_name = "instructor/courses.html"
        elif user.is_student:
            course_list = Course.objects.filter(students__id__exact=user.id).order_by(
                "-date_created"
            )
            template_name = "student/courses.html"
        else:
            course_list = []
            template_name = "student/courses.html"

        paginator = Paginator(course_list, 10)
        try:
            courses = paginator.page(page)
        except PageNotAnInteger:
            courses = paginator.page(1)
        except EmptyPage:
            courses = paginator.page(paginator.num_pages)

        context = {"courses": courses}
        return render(request, template_name, context)


@method_decorator([teacher_required], name="dispatch")
class CourseCreateView(CreateView):
    form_class = CreateCourse
    template_name = "instructor/create-course.html"

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        teacher = self.request.user
        if form.is_valid():
            title = form.cleaned_data.get("title")
            level = form.cleaned_data.get("level")
            language = form.cleaned_data.get("language")
            price = form.cleaned_data.get("price")
            description = form.cleaned_data.get("description")
            thumbnail = form.cleaned_data.get("thumbnail")
            course = Course(
                title=title,
                level=level,
                language=language,
                description=description,
                price=price,
                thumbnail=thumbnail,
                teacher=teacher,
            )
            course.save()
            UserLog.objects.create(
                action=f"Created {title} course", user_type="Instructeur", user=teacher
            )
            return redirect("dashboard:courses")

        return render(request, self.template_name, {"form": form})


class CourseDeleteView(DeleteView):
    # specify the model you want to use
    model = Course

    # can specify success url
    # url to redirect after sucessfully
    # deleting object
    success_url = reverse_lazy("dashboard:courses")


@method_decorator([teacher_required], name="dispatch")
class TutorialListView(ListView):
    template_name = "instructor/tutorials.html"

    def get(self, request, *args, **kwargs):
        user = self.request.user
        page = request.GET.get("page", 1)

        tutorial_list = Post.objects.filter(author=user).order_by("-publish_date")
        paginator = Paginator(tutorial_list, 10)
        try:
            tutorials = paginator.page(page)
        except PageNotAnInteger:
            tutorials = paginator.page(1)
        except EmptyPage:
            tutorials = paginator.page(paginator.num_pages)

        context = {"tutorials": tutorials}
        return render(request, self.template_name, context)


@method_decorator([teacher_required], name="dispatch")
class TutorialCreateView(CreateView):
    form_class = CreatePostForm
    template_name = "instructor/create-tutorial.html"

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        user = self.request.user
        if form.is_valid():
            title = form.cleaned_data.get("title")
            content = form.cleaned_data.get("content")
            description = form.cleaned_data.get("description")
            image = form.cleaned_data.get("image")
            post = Post(
                title=title,
                content=content,
                description=description,
                image=image,
                author=user,
            )
            post.save()
            UserLog.objects.create(
                action=f"Created {title} post", user_type="Instructeur", user=user
            )
            return redirect("dashboard:tutorials")

        return render(request, self.template_name, {"form": form})
