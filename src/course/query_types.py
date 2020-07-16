from graphene_django import DjangoObjectType
from .models import Course, Chapter, Lesson, Category


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


class CategoryType(DjangoObjectType):
    class Meta:
        model = Category
