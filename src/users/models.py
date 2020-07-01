from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _
from .managers import CustomUserManager
from xarala.utils import upload_image_path


class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(_("email address"), unique=True)
    is_student = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)
    is_writer = models.BooleanField(default=False)
    phone = models.CharField(max_length=150, blank=True, null=True)
    address = models.CharField(max_length=250, blank=True, null=True)
    avatar = models.ImageField(upload_to=upload_image_path, null=True, blank=True)
    bio = models.TextField(blank=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email


class Social(models.Model):
    user = models.ForeignKey(
        CustomUser, models.SET_NULL, null=True, blank=True, related_name="socials"
    )
    title = models.CharField(max_length=50, null=True, blank=True)
    link = models.URLField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.title
