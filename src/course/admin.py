from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from .models import Course, Chapter, Lesson, Category


class LessonAdmin(SummernoteModelAdmin):
    summernote_fields = ('text',)


admin.site.register(Course)
admin.site.register(Chapter)
admin.site.register(Lesson, LessonAdmin)
admin.site.register(Category)
