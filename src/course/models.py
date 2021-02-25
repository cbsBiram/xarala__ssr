from django.db import models
from django.db.models import Q
from django.urls import reverse
from django.db.models import Sum
from django.utils.text import slugify
from course.managers import CourseManager, LessonManager
from users.models import CustomUser
from xarala.utils import upload_image_path
from xarala.constants import (
    YOUTUBE,
    VIMEO,
    CLOUDINARY,
    CUSTOM,
    WISTA,
    BEGINNER,
    INTERMEDIATE,
    MEDIUM,
    ALL_LEVELS,
)
from .fields import OrderField


class Language(models.Model):
    name = models.CharField(max_length=50)
    abr = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.name} - {self.abr}"


class Category(models.Model):
    name = models.CharField(max_length=200)
    icon = models.CharField(max_length=50, default="uil-arrow")
    description = models.TextField()
    thumbnail = models.FileField(upload_to=upload_image_path, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"


class Course(models.Model):
    LEVEL = (
        (BEGINNER, BEGINNER),
        (MEDIUM, MEDIUM),
        (INTERMEDIATE, INTERMEDIATE),
        (ALL_LEVELS, ALL_LEVELS),
    )
    title = models.CharField(max_length=200)
    description = models.TextField()
    short_description = models.TextField(
        default="Dans ce cours, vous allez apprendre..."
    )
    discount = models.DecimalField(default=0, max_digits=13, decimal_places=2)
    price = models.DecimalField(default=0, max_digits=13, decimal_places=2)
    level = models.CharField(max_length=150, choices=LEVEL, default=BEGINNER)
    featured = models.BooleanField(default=False)
    slug = models.SlugField(max_length=200, unique=True, null=True, blank=True)
    thumbnail = models.ImageField(upload_to=upload_image_path, null=True, blank=True)
    teacher = models.ForeignKey(
        CustomUser,
        models.SET_NULL,
        null=True,
        related_name="courses_created",
        verbose_name="teacher",
    )
    students = models.ManyToManyField(
        CustomUser, related_name="courses_enrolled", blank=True
    )
    categories = models.ManyToManyField(Category, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    language = models.ForeignKey(Language, models.SET_NULL, null=True)
    drafted = models.BooleanField(default=False)
    published = models.BooleanField(default=False)
    publish_date = models.DateTimeField(auto_now_add=False, blank=True, null=True)
    promote_video = models.TextField(null=True)

    objects = CourseManager()

    class Meta:
        ordering = ["-date_created"]

    def __str__(self):
        return self.title

    def _get_unique_slug(self):
        slug = slugify(self.title)
        unique_slug = slug
        num = 1
        while Course.objects.filter(slug=unique_slug).exists():
            unique_slug = "{}-{}".format(slug, num)
            num += 1
        return unique_slug

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self._get_unique_slug()
        super().save(*args, **kwargs)

    def get_introudction(self):
        lesson = Lesson.objects.filter(chapter__in=self.get_chapters()).first()
        return lesson

    def get_chapters(self):
        chapters = Chapter.objects.filter(course=self).order_by("id")
        return chapters

    def get_lessons(self):
        lessons = Lesson.objects.filter(chapter__in=self.get_chapters()).order_by("id")
        return lessons

    def count_lessons(self):
        lessons = Lesson.objects.filter(chapter__in=self.get_chapters()).count()
        return lessons

    def count_duration(self):
        text = "Mns"
        lessons = Lesson.objects.filter(chapter__in=self.get_chapters())
        get_duration = lessons.aggregate(Sum("duration"))["duration__sum"]
        if get_duration:
            if get_duration >= 60:
                get_duration = get_duration / 60
                text = " Hrs"
        else:
            get_duration = 0
        return f"{round(get_duration,2)} {text}"

    def count_students(self):
        total_students = self.students.count()
        return total_students

    def get_absolute_url(self):
        return reverse("course:course-overview", kwargs={"slug": self.slug})


class Chapter(models.Model):
    name = models.CharField(max_length=150)
    course = models.ForeignKey(
        Course, models.SET_NULL, null=True, related_name="course_chapters"
    )
    slug = models.SlugField(max_length=200, unique=True, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    drafted = models.BooleanField(default=False)
    order = OrderField(blank=True, null=True, for_fields=["course"])

    def __str__(self):
        return self.name

    def _get_unique_slug(self):
        slug = slugify(self.name)
        unique_slug = slug
        num = 1
        while Chapter.objects.filter(slug=unique_slug).exists():
            unique_slug = "{}-{}".format(slug, num)
            num += 1
        return unique_slug

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self._get_unique_slug()
        super().save(*args, **kwargs)

    class Meta:
        ordering = ["id"]


class Lesson(models.Model):

    PLATFORM = (
        (YOUTUBE, YOUTUBE),
        (VIMEO, VIMEO),
        (WISTA, WISTA),
        (CUSTOM, CUSTOM),
        (CLOUDINARY, CLOUDINARY),
    )
    title = models.CharField(max_length=200)
    is_video = models.BooleanField(default=True)
    text = models.TextField(blank=True)
    order = OrderField(blank=True, null=True, for_fields=["chapter"])
    slug = models.SlugField(max_length=200, unique=True, null=True, blank=True)
    file = models.FileField(upload_to=upload_image_path, blank=True, null=True)
    video_url = models.CharField(max_length=240, null=True, blank=True)
    video_id = models.CharField(max_length=150, null=True, blank=True)
    duration = models.IntegerField(default=0)
    platform = models.CharField(max_length=50, choices=PLATFORM, default=YOUTUBE)
    chapter = models.ForeignKey(
        Chapter, models.SET_NULL, null=True, blank=True, related_name="course_lessons"
    )
    drafted = models.BooleanField(default=False)
    preview = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    objects = LessonManager()

    def __str__(self):
        return self.title

    def _get_unique_slug(self):
        slug = slugify(self.title)
        unique_slug = slug
        num = 1
        while Lesson.objects.filter(slug=unique_slug).exists():
            unique_slug = "{}-{}".format(slug, num)
            num += 1
        return unique_slug

    def next(self):
        try:
            next_lesson = Lesson.objects.filter(
                Q(
                    lecture_number=self.lecture_number + 1,
                    chapter__course__id=self.chapter.course.id,
                    chapter__id=self.chapter.id,
                )
            )
            return next_lesson.get().slug
        except Exception:
            return None

    def previous(self):
        try:
            previous_lesson = Lesson.objects.filter(
                Q(
                    lecture_number=self.lecture_number - 1,
                    chapter__course__id=self.chapter.course.id,
                    chapter__id=self.chapter.id,
                )
            )
            return previous_lesson.get().slug
        except Exception:
            return None

    class Meta:
        ordering = ["id"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self._get_unique_slug()
        super().save(*args, **kwargs)
