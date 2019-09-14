from django.db import models
from xarala.utils import upload_image_path


class Speaker(models.Model):
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    title = models.CharField(max_length=150, null=True, blank=True)
    email = models.EmailField(unique=True, null=True, blank=True)
    avatar = models.ImageField(
        upload_to=upload_image_path, null=True, blank=True)

    def __str__(self):
        return self.first_name


class Event(models.Model):
    title = models.CharField(max_length=240)
    description = models.TextField()
    place = models.CharField(max_length=240)
    total_seats = models.IntegerField(default=0)
    date_created = models.DateTimeField(auto_now_add=True)
    date_start = models.DateTimeField(
        auto_now_add=False, blank=True, null=True)
    date_end = models.DateTimeField(
        auto_now_add=False, blank=True, null=True)
    speakers = models.ManyToManyField(Speaker, blank=True)

    def __str__(self):
        return self.title
