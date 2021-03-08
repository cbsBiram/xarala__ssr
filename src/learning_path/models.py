from django.db import models
from django.utils.text import slugify
from django.urls import reverse
from learning_path.managers import LearningPathManager
from xarala.utils import upload_image_path
from xarala.constants import COURSE, TUTORIAL
from course.models import Course
from blog.models import Post


class LearningPath(models.Model):
    PATH_CHOICES = (
        (COURSE, COURSE),
        (TUTORIAL, TUTORIAL),
    )
    title = models.CharField(max_length=60)
    slug = models.SlugField(max_length=200, unique=True, null=True, blank=True)
    thumbnail = models.ImageField(upload_to=upload_image_path, null=True)
    description = models.TextField()
    path_type = models.CharField(max_length=10, choices=PATH_CHOICES)
    courses = models.ManyToManyField(Course)
    tutorials = models.ManyToManyField(Post)
    published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = LearningPathManager()

    class Meta:
        ordering = ["-updated_at"]

    def __str__(self):
        return self.title

    def _get_unique_slug(self):
        slug = slugify(self.title)
        unique_slug = slug
        num = 1
        while LearningPath.objects.filter(slug=unique_slug).exists():
            unique_slug = "{}-{}".format(slug, num)
            num += 1
        return unique_slug

    def get_absolute_url(self):
        return reverse("learning-path:path-detail", kwargs={"slug": self.slug})
