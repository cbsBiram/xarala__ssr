from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from users.decorators import staff_required
from django.views.generic import (View, ListView, TemplateView)
from django.shortcuts import render
from course.models import Course
from userlogs.models import UserLog
from users.models import CustomUser


@method_decorator([login_required], name="dispatch")
class DashboardView(View):
    template_name = "dashboard/index.html"

    def get(self, request, *args, **kwargs):
        user = self.request.user
        total_courses = 0
        if user.user_type == "ST":
            total_courses = user.courses_enrolled.all().count()
        elif user.user_type == "TC":
            total_courses = user.courses_created.all().count()

        context = {"total_courses": total_courses}
        return render(request, self.template_name, context)


@method_decorator([staff_required], name="dispatch")
class StaffView(TemplateView):
    template_name = "dashboard/staff.html"
    total_courses = Course.objects.all().count()
    total_users =  CustomUser.objects.all().count()
    total_students = CustomUser.objects.filter(user_type="ST").count()
    logs = UserLog.objects.all()[:3]

    extra_context = {
        'title': 'Staff',
        'total_courses': total_courses,
        'total_users': total_users,
        'total_students': total_students,
        'logs': logs,
    }


class UserLogList(ListView):
    model = UserLog
    context_object_name = 'logs'
