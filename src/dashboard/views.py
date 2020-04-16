from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import View
from django.shortcuts import render
from course.models import Course


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
