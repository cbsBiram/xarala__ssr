import graphene
from graphene_django import DjangoObjectType
from django.db.models import Q
from .models import Course, Chapter, Lesson


class CourseType(DjangoObjectType):

    class Meta:
        model = Course
        convert_choices_to_enum = False


class ChapterType(DjangoObjectType):

    class Meta:
        model = Chapter
        convert_choices_to_enum = False


class LessonType(DjangoObjectType):

    class Meta:
        model = Lesson
        convert_choices_to_enum = False
