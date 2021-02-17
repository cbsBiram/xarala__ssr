from django.db import models
from xarala.utils import upload_image_path
from users.models import CustomUser


class Guest(models.Model):
    name = models.CharField(max_length=150)
    profession = models.CharField(max_length=150)

    def __str__(self):
        return self.name


class Episode(models.Model):
    title = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    guest = models.ForeignKey(Guest, models.SET_NULL, blank=True, null=True)
    publisher = models.ForeignKey(CustomUser, models.SET_NULL, blank=True, null=True)
    embed = models.TextField(blank=True)
    thumbnail = models.ImageField(upload_to=upload_image_path, null=True, blank=True)
    published_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.title
