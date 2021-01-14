from django.db.models import Q
import graphene
from graphql import GraphQLError
from graphql_jwt.decorators import login_required

from course.services.course_svc import get_language_by_name, get_languages
from .models import Category, Chapter, Course, Lesson
from .query_types import CategoryType, ChapterType, CourseType, LanguageType, LessonType


class Query(graphene.ObjectType):
    courses = graphene.List(CourseType, search=graphene.String())
    course = graphene.Field(CourseType, courseSlug=graphene.String(), required=True)
    courseLesson = graphene.Field(CourseType, courseSlug=graphene.String())
    chapters = graphene.List(ChapterType, search=graphene.String())
    chapter = graphene.Field(ChapterType, chapterId=graphene.Int())
    lessons = graphene.List(LessonType, search=graphene.String())
    lesson = graphene.Field(LessonType, lessonId=graphene.Int())
    categories = graphene.List(CategoryType, search=graphene.String())
    category = graphene.Field(CategoryType, categoryName=graphene.Int())
    languages = graphene.List(LanguageType, search=graphene.String())
    language = graphene.Field(LanguageType, categoryName=graphene.Int())

    def resolve_courses(self, info, search=None):
        if search:
            filter = Q(title__icontains=search) | Q(description__icontains=search)
            return Course.objects.filter(filter)
        return Course.objects.all()

    def resolve_course(self, info, courseSlug):
        """ Course preview """
        course = Course.objects.get(slug=courseSlug)
        return course

    @login_required
    def resolve_courseLesson(self, info, courseSlug):
        """ Course Lecture, the user must be logged in and enrolled it """
        user = info.context.user
        course = Course.objects.get(slug=courseSlug)
        if course not in user.courses_enrolled.all():
            raise GraphQLError("You're not authorized to see this course!")
        return course

    def resolve_chapters(self, info, search=None):
        if search:
            filter = Q(name__icontains=search) | Q(course__title__icontains=search)
            return Chapter.objects.filter(filter)
        return Chapter.objects.all()

    def resolve_chapter(self, info, chapterId):
        chapter = Chapter.objects.get(pk=chapterId)
        return chapter

    def resolve_lessons(self, info, search=None):
        if search:
            filter = Q(title__icontains=search) | Q(chapter__name__icontains=search)
            return Lesson.objects.filter(filter)
        return Lesson.objects.all()

    def resolve_lesson(self, info, lessonId):
        lesson = Lesson.objects.get(pk=lessonId)
        return lesson

    def resolve_categories(self, info, search=None):
        if search:
            filter = Q(name__icontains=search) | Q(description__icontains=search)
            return Category.objects.filter(filter)
        return Category.objects.all()

    def resolve_category(self, info, categoryName):
        category = Category.objects.filter(name=categoryName)
        return category

    def resolve_languages(self, info, search=None):
        return get_languages(search=search)

    def resolve_language(self, info, languageName):
        return get_language_by_name(languageName)


# new product


class CreateCourse(graphene.Mutation):
    course = graphene.Field(CourseType)

    class Arguments:
        title = graphene.String()
        description = graphene.Int()
        price = graphene.Float()
        level = graphene.String()
        thumbnail = graphene.String()
        language = graphene.String()

    def mutate(self, info, title, description, price, level, thumbnail, language):
        user = info.context.user
        if user.is_anonymous:
            raise GraphQLError("Log in to add a course!")

        course = Course(
            title=title,
            description=description,
            price=price,
            level=level,
            thumbnail=thumbnail,
            language=language,
            teacher=user,
        )
        course.save()
        return CreateCourse(course=course)


# update track


class UpdateCourse(graphene.Mutation):
    course = graphene.Field(CourseType)

    class Arguments:
        courseId = graphene.Int(required=True)
        title = graphene.String()
        description = graphene.Int()
        price = graphene.Float()
        level = graphene.String()
        thumbnail = graphene.String()
        language = graphene.String()

    def mutate(
        self, info, courseId, title, description, price, level, thumbnail, language
    ):
        user = info.context.user
        if user.is_anonymous:
            raise GraphQLError("Log in to edit a track!")
        course = Course.objects.get(id=courseId)
        if course.owner != user:
            raise GraphQLError("Not permited to update this track")
        course.title = title
        course.description = description
        course.price = price
        course.level = level
        course.thumbnail = thumbnail
        course.language = language
        course.save()
        return UpdateCourse(course=course)


# delete course


class DeleteCourse(graphene.Mutation):
    courseId = graphene.Int()

    class Arguments:
        courseId = graphene.Int(required=True)

    def mutate(self, info, courseId):
        user = info.context.user
        course = Course.objects.get(id=courseId)
        if course.teacher != user:
            raise GraphQLError("Not permited to update this course")
        Course.objects.filter(id=courseId).update(drafted=True)
        return DeleteCourse(courseId=courseId)


# subscribe user to course


class SubscribeUserToCourse(graphene.Mutation):
    course = graphene.Field(CourseType)

    class Arguments:
        courseId = graphene.Int(required=True)

    def mutate(self, info, courseId):
        user = info.context.user
        if not user:
            raise GraphQLError("Vous n'etes pas connecté")
        course = Course.objects.get(pk=courseId)
        if course not in user.courses_enrolled.all():
            user.courses_enrolled.add(course)
            return SubscribeUserToCourse(course=course)
        return SubscribeUserToCourse(course=course)


class Mutation(graphene.ObjectType):
    create_course = CreateCourse.Field()
    update_course = UpdateCourse.Field()
    delete_course = DeleteCourse.Field()
    subscribe_user_to_course = SubscribeUserToCourse.Field()
