from course.models import Course
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.generic import ListView, View
from userlogs.models import UserLog
from users.decorators import staff_required
from users.models import CustomUser


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
