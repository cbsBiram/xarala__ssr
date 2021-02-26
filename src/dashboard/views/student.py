from django.utils.decorators import method_decorator
from course.models import Course
from users.decorators import student_required
from django.views.generic import View
from django.shortcuts import render


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
