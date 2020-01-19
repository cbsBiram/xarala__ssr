import graphene
from graphql import GraphQLError
from .models import Course, Chapter, Lesson
from .query_types import CourseType, ChapterType, LessonType, Q


class Query(graphene.ObjectType):
    courses = graphene.List(CourseType, search=graphene.String())
    course = graphene.Field(CourseType, courseId=graphene.Int())
    chapters = graphene.List(ChapterType, search=graphene.String())
    chapter = graphene.Field(ChapterType, chapterId=graphene.Int())
    lessons = graphene.List(LessonType, search=graphene.String())
    lesson = graphene.Field(LessonType, lessonId=graphene.Int())

    def resolve_courses(self, info, search=None):
        if search:
            filter = (
                Q(title__icontains=search) |
                Q(description__icontains=search)
            )
            return Course.objects.filter(filter)
        return Course.objects.all()

    def resolve_course(self, info, courseId):
        course = Course.objects.get(pk=courseId)
        return course

    def resolve_chapters(self, info, search=None):
        if search:
            filter = (
                Q(name__icontains=search) |
                Q(course__title__icontains=search)
            )
            return Chapter.objects.filter(filter)
        return Chapter.objects.all()

    def resolve_chapter(self, info, chapterId):
        chapter = Chapter.objects.get(pk=chapterId)
        return chapter

    def resolve_lessons(self, info, search=None):
        if search:
            filter = (
                Q(title__icontains=search) |
                Q(chapter__name__icontains=search)
            )
            return Lesson.objects.filter(filter)
        return Lesson.objects.all()

    def resolve_lesson(self, info, lessonId):
        lesson = Lesson.objects.get(pk=lessonId)
        return lesson

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
            teacher=user
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

    def mutate(self, info,  courseId, title, description, price, level, thumbnail, language):
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
        Course.objects.filter(id=courseId).update(
            drafted=True
        )
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
        if course not in student.courses_enrolled.all():
            student.courses_enrolled.add(course)


class Mutation(graphene.ObjectType):
    create_course = CreateCourse.Field()
    update_course = UpdateCourse.Field()
    delete_course = DeleteCourse.Field()
