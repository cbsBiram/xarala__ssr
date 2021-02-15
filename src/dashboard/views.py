from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from users.decorators import staff_required
from django.views.generic import View, ListView
from django.shortcuts import render
from course.models import Course
from userlogs.models import UserLog
from users.models import CustomUser
from blog.models import Post


@method_decorator([login_required], name="dispatch")
class DashboardView(View):
    template_name = "dashboard.html"

    def get(self, request, *args, **kwargs):
        user = self.request.user
        total_courses = 0
        total_posts = Post.objects.count()
        if user.is_student:
            total_courses = user.courses_enrolled.all().count()
        elif user.is_teacher:
            total_courses = user.courses_created.all().count()

        context = {"total_courses": total_courses, "total_posts": total_posts}
        return render(request, self.template_name, context)


@method_decorator([staff_required], name="dispatch")
class StaffView(View):
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
