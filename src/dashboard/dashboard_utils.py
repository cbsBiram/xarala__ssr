from django.utils.text import slugify
from course.models import Chapter, Lesson


def slugify_chapter(name):
    slug = slugify(name)
    unique_slug = slug
    num = 1
    while Chapter.objects.filter(slug=unique_slug).exists():
        unique_slug = "{}-{}".format(slug, num)
        num += 1
    return unique_slug


def slugify_lesson(title):
    slug = slugify(title)
    unique_slug = slug
    num = 1
    while Lesson.objects.filter(slug=unique_slug).exists():
        unique_slug = "{}-{}".format(slug, num)
        num += 1
    return unique_slug
