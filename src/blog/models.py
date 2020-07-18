from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from xarala.utils import upload_image_path
from users.models import CustomUser


class Tag(models.Model):
    name = models.CharField(max_length=150, blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name_plural = "tags"

    def __str__(self):
        return self.name


class Post(models.Model):
    author = models.ForeignKey(CustomUser, models.SET_NULL, null=True, blank=True,)
    title = models.CharField(max_length=150)
    content = models.TextField(blank=True, null=True)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    image = models.ImageField(upload_to=upload_image_path, blank=True, null=True)
    image_url = models.URLField(max_length=255, blank=True, null=True)
    published = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)
    date_published = models.DateTimeField(auto_now_add=False, blank=True, null=True)
    date_updated = models.DateTimeField(auto_now_add=False, blank=True, null=True)
    featured = models.BooleanField(default=False)
    drafted = models.BooleanField(default=False)
    tags = models.ManyToManyField(Tag, blank=True)

    def __str__(self):
        return self.title

    def _get_unique_slug(self):
        slug = slugify(self.title)
        unique_slug = slug
        num = 1
        while Post.objects.filter(slug=unique_slug).exists():
            unique_slug = "{}-{}".format(slug, num)
            num += 1
        return unique_slug

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self._get_unique_slug()
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("blog:blog-detail", kwargs={"slug": self.slug})
