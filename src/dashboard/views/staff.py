from course.models import Course
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.generic import ListView, View
from userlogs.models import UserLog
from users.decorators import staff_required
from users.models import CustomUser


@method_decorator([staff_required], name="dispatch")
class UserLogList(ListView):
    model = UserLog
    context_object_name = "logs"
    template_name = "staff/logs.html"
    paginate_by = 20


@method_decorator([staff_required], name="dispatch")
class StaffView(View):
    template_name = "staff/dashboard.html"

    def get(self, request, *args, **kwargs):
        total_courses = Course.objects.count()
        total_teachers = CustomUser.objects.filter(is_teacher=True).count()
        total_students = CustomUser.objects.filter(is_student=True).count()

        context = {
            "title": "Staff",
            "total_courses": total_courses,
            "total_teachers": total_teachers,
            "total_students": total_students,
        }
        return render(request, self.template_name, context)


@method_decorator([staff_required], name="dispatch")
class AllCoursesView(ListView):
    queryset = Course.objects.all()
    context_object_name = "courses"
    paginate_by = 20
    template_name = "staff/all_courses.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


@method_decorator([staff_required], name="dispatch")
class PublishedCoursesView(ListView):
    queryset = Course.objects.published()
    context_object_name = "courses"
    paginate_by = 20
    template_name = "staff/published_courses.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


@method_decorator([staff_required], name="dispatch")
class UnPublishedCoursesView(ListView):
    queryset = Course.objects.unpublished()
    context_object_name = "courses"
    paginate_by = 20
    template_name = "staff/unpublished_courses.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
