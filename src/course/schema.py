from django.db.models import Q
import graphene
from graphql import GraphQLError
from graphql_jwt.decorators import context, login_required

from course.services.course_svc import get_language_by_name, get_languages
from users.upload import save_base_64
from xarala.utils import get_paginator
from .models import Category, Chapter, Course, Language, Lesson
from .query_types import (
    CategoryType,
    ChapterType,
    CourseType,
    LanguageType,
    LessonType,
    CoursePaginatedType,
)


class Query(graphene.ObjectType):
    allCourses = graphene.Field(
        CoursePaginatedType, search=graphene.String(), page=graphene.Int()
    )
    courses = graphene.List(CourseType, search=graphene.String())
    latestCourses = graphene.List(CourseType, search=graphene.String())
    course = graphene.Field(CourseType, courseSlug=graphene.String(), required=True)
    courseLesson = graphene.Field(CourseType, courseSlug=graphene.String())
    chapters = graphene.List(ChapterType, search=graphene.String())
    chaptersCourse = graphene.List(
        ChapterType, courseSlug=graphene.String(required=True)
    )
    chaptersUser = graphene.List(ChapterType)
    chapterCourse = graphene.Field(
        ChapterType,
        courseSlug=graphene.String(required=True),
        chapterSlug=graphene.String(required=True),
    )
    chapter = graphene.Field(ChapterType, chapterId=graphene.Int())
    lessons = graphene.List(LessonType, search=graphene.String())
    lessonsChapter = graphene.List(
        LessonType,
        courseSlug=graphene.String(required=True),
        chapterSlug=graphene.String(required=True),
    )
    lessonChapter = graphene.Field(
        LessonType,
        courseSlug=graphene.String(required=True),
        chapterSlug=graphene.String(required=True),
        lessonSlug=graphene.String(required=True),
    )
    lesson = graphene.Field(LessonType, lessonSlug=graphene.String(required=True))
    categories = graphene.List(CategoryType, search=graphene.String())
    category = graphene.Field(CategoryType, categoryName=graphene.Int())
    languages = graphene.List(LanguageType, search=graphene.String())
    language = graphene.Field(LanguageType, categoryName=graphene.Int())
    checkEnrollement = graphene.Boolean(courseId=graphene.Int(required=True))

    def resolve_courses(self, info, search=None):
        if search:
            filter = Q(title__icontains=search) | Q(description__icontains=search)
            return Course.objects.filter(filter)
        return Course.objects.all()

    def resolve_allCourses(self, info, page, search=None):
        page_size = 10
        if search:
            filter = Q(title__icontains=search) | Q(description__icontains=search)
            courses = Course.objects.filter(filter)
            return get_paginator(courses, page_size, page, CoursePaginatedType)
        return get_paginator(
            Course.objects.published(), page_size, page, CoursePaginatedType
        )

    def resolve_latestCourses(self, info, search=None):
        if search:
            filter = Q(title__icontains=search) | Q(description__icontains=search)
            return Course.objects.filter(filter)
        return Course.objects.order_by("-id")[:3]

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

    def resolve_chaptersCourse(self, info, courseSlug):
        user = info.context.user
        if user.is_anonymous:
            raise GraphQLError("You must log in!")
        chapters = Chapter.objects.filter(course__slug=courseSlug)
        return chapters

    def resolve_chapters(self, info, search=None):
        if search:
            filter = Q(name__icontains=search) | Q(course__title__icontains=search)
            return Chapter.objects.filter(filter)
        return Chapter.objects.all()

    def resolve_chapterCourse(self, info, courseSlug, chapterSlug):
        user = info.context.user
        if user.is_anonymous:
            raise GraphQLError("You must log in!")
        chapter = Chapter.objects.get(Q(slug=chapterSlug) & Q(course__slug=courseSlug))
        return chapter

    def resolve_chaptersUser(self, info):
        user = info.context.user
        if user.is_anonymous or user.is_writer:
            raise GraphQLError("You must log in as a student or a teacher!")
        chapters = {}
        if user.is_student:
            chapters = Chapter.objects.filter(course__teacher=user)
        else:
            chapters = Chapter.objects.filter(
                course__students__id__exact=user.id, allowed=True
            )
        return chapters

    def resolve_chapter(self, info, chapterId):
        chapter = Chapter.objects.get(pk=chapterId)
        return chapter

    def resolve_lessons(self, info, search=None):
        if search:
            filter = Q(title__icontains=search) | Q(chapter__name__icontains=search)
            return Lesson.objects.filter(filter)
        return Lesson.objects.all()

    def resolve_lessonsChapter(self, info, courseSlug, chapterSlug):
        user = info.context.user
        if user.is_anonymous:
            raise GraphQLError("You must log in!")
        chapter = Chapter.objects.get(Q(slug=chapterSlug) & Q(course__slug=courseSlug))
        return chapter.course_lessons.all()

    def resolve_lessonChapter(self, info, courseSlug, chapterSlug, lessonSlug):
        user = info.context.user
        if user.is_anonymous:
            raise GraphQLError("You must log in!")
        chapter = Chapter.objects.get(Q(slug=chapterSlug) & Q(course__slug=courseSlug))
        lesson = Lesson.objects.get(Q(chapter=chapter) & Q(slug=lessonSlug))
        return lesson

    @login_required
    def resolve_lesson(self, info, lessonSlug):
        lesson = Lesson.objects.get(slug=lessonSlug)
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

    @login_required
    def resolve_checkEnrollement(self, info, courseId):
        user = info.context.user
        if user.is_anonymous:
            raise GraphQLError("Log in to enroll this course")
        course = Course.objects.get(pk=courseId)
        if course not in user.courses_enrolled.all():
            return False
        return True


# new product
class CreateCourse(graphene.Mutation):
    course = graphene.Field(CourseType)

    class Arguments:
        title = graphene.String(required=True)
        description = graphene.String()
        price = graphene.Decimal()
        level = graphene.String(required=True)
        file = graphene.String()
        languageName = graphene.String(required=True)

    def mutate(self, info, title, description, price, level, file, languageName):
        user = info.context.user
        if user.is_anonymous:
            raise GraphQLError("Log in to add a course!")

        language = Language.objects.get(name=languageName)
        final_file_url = save_base_64(file)
        course = Course(
            title=title,
            description=description,
            price=price,
            level=level,
            thumbnail=final_file_url,
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
        description = graphene.String()
        price = graphene.Decimal()
        level = graphene.String()
        file = graphene.String()
        languageName = graphene.String()

    def mutate(
        self, info, courseId, title, description, price, level, file, languageName
    ):
        user = info.context.user
        if user.is_anonymous:
            raise GraphQLError("Log in to edit a track!")
        course = Course.objects.get(id=courseId)
        if course.teacher != user:
            raise GraphQLError("Not permited to update this track")
        if title:
            course.title = title
        if description:
            course.description = description
        if price:
            course.price = price
        if level:
            course.level = level
        if file:
            final_file_url = save_base_64(file)
            course.thumbnail = final_file_url
        if languageName:
            language = Language.objects.get(name=languageName)
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


# create a section for a specific course
class CreateChapter(graphene.Mutation):
    chapter = graphene.Field(ChapterType)

    class Arguments:
        courseSlug = graphene.String(required=True)
        name = graphene.String(required=True)

    def mutate(self, info, courseSlug, name):
        user = info.context.user
        if user.is_anonymous:
            raise GraphQLError("Log in to add a chapter/section!")

        course = Course.objects.get(slug=courseSlug)
        chapter = Chapter(name=name, course=course)
        chapter.save()

        return CreateChapter(chapter=chapter)


# update a section for a specific course
class UpdateChapter(graphene.Mutation):
    chapter = graphene.Field(ChapterType)

    class Arguments:
        chapterId = graphene.Int(required=True)
        name = graphene.String()
        chapterNumber = graphene.Int()

    def mutate(self, info, chapterId, name, chapterNumber):
        user = info.context.user
        print("chapter number", chapterNumber)
        if user.is_anonymous:
            raise GraphQLError("Log in to update a chapter/section!")

        chapter = Chapter.objects.get(pk=chapterId)
        chapter.name = name
        chapter.chapter_number = chapterNumber
        chapter.save()

        return UpdateChapter(chapter=chapter)


# create a lesson for a specific chapter
class CreateLesson(graphene.Mutation):
    lesson = graphene.Field(LessonType)

    class Arguments:
        courseSlug = graphene.String(required=True)
        chapterSlug = graphene.String(required=True)
        title = graphene.String(required=True)
        videoId = graphene.String(required=True)
        duration = graphene.Int()
        platform = graphene.String(required=True)

    def mutate(self, info, courseSlug, chapterSlug, title, videoId, duration, platform):
        user = info.context.user
        if user.is_anonymous:
            raise GraphQLError("Log in to add a lesson!")

        chapter = Chapter.objects.get(Q(course__slug=courseSlug) & Q(slug=chapterSlug))
        lesson = Lesson(
            title=title,
            duration=duration,
            platform=platform,
            chapter=chapter,
            video_id=videoId,
        )
        lesson.save()

        return CreateLesson(lesson=lesson)


# update a lesson for a specific chapter
class UpdateLesson(graphene.Mutation):
    lesson = graphene.Field(LessonType)

    class Arguments:
        lessonId = graphene.Int(required=True)
        title = graphene.String()
        videoId = graphene.String()
        duration = graphene.Int()
        platform = graphene.String()
        lectureNumber = graphene.Int(required=True)

    def mutate(self, info, lessonId, title, videoId, duration, platform, lectureNumber):
        user = info.context.user
        if user.is_anonymous:
            raise GraphQLError("Log in to update a lesson!")

        lesson = Lesson.objects.get(pk=lessonId)
        lesson.title = title
        lesson.video_id = videoId
        lesson.duration = duration
        lesson.platform = platform
        lesson.lecture_number = lectureNumber
        lesson.save()

        return UpdateLesson(lesson=lesson)


class Mutation(graphene.ObjectType):
    create_course = CreateCourse.Field()
    update_course = UpdateCourse.Field()
    delete_course = DeleteCourse.Field()
    subscribe_user_to_course = SubscribeUserToCourse.Field()
    create_chapter = CreateChapter.Field()
    update_chapter = UpdateChapter.Field()
    create_lesson = CreateLesson.Field()
    update_lesson = UpdateLesson.Field()
