from django import template

from course.models import Course

register = template.Library()


@register.simple_tag
def enroll_button(course_id, student):
    button_text = "Poursuivre"
    course = Course.objects.get(pk=course_id)
    if student.is_authenticated and course in student.courses_enrolled.all():
        pass
    else:
        button_text = "Enroller"
    return button_text
