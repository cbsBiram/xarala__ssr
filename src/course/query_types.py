import graphene
from graphene_django import DjangoObjectType
from .models import Course, Chapter, Lesson, Category, Language


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

    get_previous = graphene.Field(graphene.String)
    get_next = graphene.Field(graphene.String)

    def resolve_get_previous(instance, info, **kwargs):
        return instance.previous()

    def resolve_get_next(instance, info, **kwargs):
        return instance.next()


class CategoryType(DjangoObjectType):
    class Meta:
        model = Category


class LanguageType(DjangoObjectType):
    class Meta:
        model = Language


class CoursePaginatedType(graphene.ObjectType):
    page = graphene.Int()
    pages = graphene.Int()
    has_next = graphene.Boolean()
    has_prev = graphene.Boolean()
    objects = graphene.List(CourseType)
