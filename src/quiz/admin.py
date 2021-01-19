from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from .models import Quiz, Question, Answer, UserAnswer


class QuizAdmin(SummernoteModelAdmin):
    summernote_fields = ("content")

class QuestionAdmin(SummernoteModelAdmin):
    summernote_fields = ("content")

class AnswerAdmin(SummernoteModelAdmin):
    summernote_fields = ("content")

class UserAnswerAdmin(SummernoteModelAdmin):
    summernote_fields = ("content")

class ResultAdmin(SummernoteModelAdmin):
    summernote_fields = ("content")

admin.site.register(Quiz, QuizAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer, AnswerAdmin)
admin.site.register(UserAnswer, UserAnswerAdmin)
