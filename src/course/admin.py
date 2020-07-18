from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin

from .models import Course, Chapter, Lesson, Category, Language


class LessonAdmin(SummernoteModelAdmin):
    summernote_fields = ("text",)


class CourseAdmin(SummernoteModelAdmin):
    summernote_fields = (
        "description",
        "projects",
        "what_will_i_learn",
        "requirements",
        "target_audience",
    )


admin.site.register(Course, CourseAdmin)
admin.site.register(Chapter)
admin.site.register(Lesson, LessonAdmin)
admin.site.register(Category)
admin.site.register(Language)
