from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.utils.text import slugify
from xarala.utils import upload_image_path
from users.models import CustomUser
from .managers import BlogPostManager


class Tag(models.Model):
    name = models.CharField(max_length=150, blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name_plural = "tags"

    def __str__(self):
        return self.name

    def tag_posts(self):
        return self.post_set.filter(drafted=False)


class Post(models.Model):
    author = models.ForeignKey(
        CustomUser,
        models.SET_NULL,
        null=True,
        blank=True,
    )
    title = models.CharField(max_length=150)
    content = models.TextField(blank=True, null=True)
    description = models.TextField(default="dans cet article, vous allez...")
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    image = models.ImageField(upload_to=upload_image_path, blank=True, null=True)
    image_url = models.URLField(max_length=255, blank=True, null=True)
    published = models.BooleanField(default=False)
    submitted = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    publish_date = models.DateTimeField(auto_now_add=False, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)
    featured = models.BooleanField(default=False)
    drafted = models.BooleanField(default=False)
    tags = models.ManyToManyField(Tag, blank=True)

    objects = BlogPostManager()

    class Meta:
        ordering = ["-publish_date", "-updated_at", "-timestamp"]

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

    def next(self):
        try:
            return Post.objects.published().get(id=self.id + 1).slug
        except Exception:
            return None

    def previous(self):
        try:
            return Post.objects.published().get(id=self.id - 1).slug
        except Exception:
            return None
