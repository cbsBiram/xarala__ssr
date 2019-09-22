from django.db import models
from django.utils.text import slugify
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
    description = models.TextField(null=True)
    content = models.TextField(null=True, blank=True)
    location = models.CharField(max_length=240)
    country = models.CharField(max_length=240, null=True)
    total_seats = models.IntegerField(default=0)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    image = models.ImageField(
        upload_to=upload_image_path, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_start = models.DateTimeField(
        auto_now_add=False, blank=True, null=True)
    date_end = models.DateTimeField(
        auto_now_add=False, blank=True, null=True)
    speakers = models.ManyToManyField(Speaker, blank=True)

    def __str__(self):
        return self.title

    def _get_unique_slug(self):
        slug = slugify(self.title)
        unique_slug = slug
        num = 1
        while Event.objects.filter(slug=unique_slug).exists():
            unique_slug = '{}-{}'.format(slug, num)
            num += 1
        return unique_slug

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self._get_unique_slug()
        super().save(*args, **kwargs)
