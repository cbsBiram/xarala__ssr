from django.contrib.auth.decorators import login_required
from django.db.models.aggregates import Count, Sum
from django.utils.decorators import method_decorator
from users.decorators import staff_required, teacher_required
from django.views.generic import View, ListView
from django.shortcuts import redirect, render
from course.models import Course
from userlogs.models import UserLog
from users.models import CustomUser


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


@teacher_required
def instructor_dashboard(request):
    instructor = request.user
    courses_published = Course.objects.filter(teacher=instructor, published=True)
    total_sales = courses_published.aggregate(Sum("price"))["price__sum"]
    total_enroll = courses_published.aggregate(Count("students"))["students__count"]
    courses_unpublished = Course.objects.filter(teacher=instructor, published=False)

    return render(
        request,
        "instructor/dashboard.html",
        {
            "total_sales": total_sales,
            "total_enroll": total_enroll,
            "courses_published": courses_published,
            "courses_unpublished": courses_unpublished,
        },
    )
