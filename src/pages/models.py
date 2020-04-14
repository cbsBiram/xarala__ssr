from django.db import models
from django.utils import timezone
from xarala.utils import upload_image_path


class Subscribe(models.Model):
    email_id = models.EmailField(null=True, blank=True)
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.email_id


class Carousel(models.Model):
    title = models.CharField(max_length=150)
    link_to = models.URLField(max_length=200)
    link_text = models.CharField(max_length=50)
    image = models.ImageField(
        upload_to=upload_image_path, null=True, blank=True)
    active = models.BooleanField(default=False)

    def __str__(self):
        return self.title
