from django.db import models
from django.db.models.signals import pre_save
from django.utils.text import slugify
from users.models import CustomUser
from xarala.utils import upload_image_path


class Category(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"


class Course(models.Model):
    # Niveaux
    BEGINNER = "Débutant"
    MEDIUM = "Moyen"
    INTERMEDIATE = "Intermédiaire"
    LEVEL = (
        (BEGINNER, BEGINNER),
        (MEDIUM, MEDIUM),
        (INTERMEDIATE, INTERMEDIATE)
    )
    title = models.CharField(max_length=200)
    description = models.TextField()
    is_free = models.BooleanField(default=True)
    price = models.DecimalField(default=0, max_digits=13, decimal_places=2)
    level = models.CharField(max_length=150, choices=LEVEL, default=BEGINNER)
    slug = models.SlugField(max_length=200, unique=True, null=True, blank=True)
    thumbnail = models.ImageField(
        upload_to=upload_image_path, null=True, blank=True)
    teacher = models.ForeignKey(
        CustomUser, models.SET_NULL, null=True, related_name='courses_created')
    students = models.ManyToManyField(
        CustomUser, related_name='courses_enrolled', blank=True)
    categories = models.ManyToManyField(Category, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def _get_unique_slug(self):
        slug = slugify(self.title)
        unique_slug = slug
        num = 1
        while Course.objects.filter(slug=unique_slug).exists():
            unique_slug = '{}-{}'.format(slug, num)
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
        chapters = Chapter.objects.filter(course=self)
        return chapters

    def get_lessons(self):
        lessons = Lesson.objects.filter(chapter__in=self.get_chapters())
        return lessons


class Chapter(models.Model):
    name = models.CharField(max_length=150)
    course = models.ForeignKey(Course, models.SET_NULL, null=True)
    slug = models.SlugField(max_length=200, unique=True, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def _get_unique_slug(self):
        slug = slugify(self.name)
        unique_slug = slug
        num = 1
        while Chapter.objects.filter(slug=unique_slug).exists():
            unique_slug = '{}-{}'.format(slug, num)
            num += 1
        return unique_slug

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self._get_unique_slug()
        super().save(*args, **kwargs)


class Lesson(models.Model):
    # platform
    YOUTUBE = "Youtube"
    VIMEO = "Vimeo"
    WISTA = "Wista"
    CUSTOM = "Custom"
    PLATFORM = (
        (YOUTUBE, YOUTUBE),
        (VIMEO, VIMEO),
        (WISTA, WISTA),
        (CUSTOM, CUSTOM)
    )
    title = models.CharField(max_length=200)
    text = models.TextField(blank=True)
    slug = models.SlugField(max_length=200, unique=True, null=True, blank=True)
    file = models.FileField(upload_to=upload_image_path, blank=True, null=True)
    resource_link = models.CharField(max_length=240, null=True, blank=True)
    video_id = models.CharField(max_length=150, null=True, blank=True)
    platform = models.CharField(
        max_length=50, choices=PLATFORM, default=YOUTUBE)
    chapter = models.ForeignKey(
        Chapter, models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.title

    def _get_unique_slug(self):
        slug = slugify(self.title)
        unique_slug = slug
        num = 1
        while Lesson.objects.filter(slug=unique_slug).exists():
            unique_slug = '{}-{}'.format(slug, num)
            num += 1
        return unique_slug

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self._get_unique_slug()
        super().save(*args, **kwargs)
