from django.db import models
from xarala.utils import upload_image_path
from course.models import Course
from blog.models import Post


class LearningPath(models.Model):
    course = (
        ("Django", "Django"),
        ("React", "React"),
        ("Python", "Python"),
    )
    title = models.CharField(max_length=60)
    thumbnail = models.ImageField(upload_to=upload_image_path, null=True, blank=True)
    description = models.TextField()
    path_type = models.CharField(max_length=60, choices=course)
    course = models.ManyToManyField(Course, blank=True)
    tutorials = models.ManyToManyField(Post, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
