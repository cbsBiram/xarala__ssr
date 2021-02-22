import pytest

from course.models import Category, Course, Language, Chapter, Lesson
from users.models import CustomUser as User


@pytest.mark.django_db
def test_language_create():
    language = Language.objects.create(
        name="Wolof",
        abr="Wf",
    )
    assert language.name == "Wolof"
    assert language.abr == "Wf"


@pytest.mark.django_db
def test_category_create():
    category = Category.objects.create(
        name="Python",
        description="Category for python",
    )
    assert category.name == "Python"
    assert category.description == "Category for python"


@pytest.mark.django_db
def test_course_create():
    teacher = User.objects.create(email="test@test.com")
    category = Category.objects.create(
        name="Python",
        description="Category for python",
    )
    language = Language.objects.create(
        name="Wolof",
        abr="Wf",
    )
    course = Course.objects.create(
        title="Python course",
        description="This is a python course",
        teacher=teacher,
        language=language,
    )
    course.categories.set([category])
    assert course.title == "Python course"
    assert course.description == "This is a python course"
    assert course.teacher == teacher
    assert course.language == language
    assert course.categories.count() == 1


@pytest.mark.django_db
def test_chapter_create():
    course = Course.objects.create(
        title="Python course",
        description="This is a python course",
    )
    chapter = Chapter.objects.create(
        name="Python course chapter",
        course=course,
    )
    assert chapter.name == "Python course chapter"
    assert chapter.course == course


@pytest.mark.django_db
def test_lesson_create():
    course = Course.objects.create(
        title="Python course",
        description="This is a python course",
    )
    chapter = Chapter.objects.create(
        name="Python course chapter",
        course=course,
    )
    lesson = Lesson.objects.create(
        title="Python chapter lesson",
        chapter=chapter,
    )
    assert lesson.title == "Python chapter lesson"
    assert lesson.chapter == chapter
