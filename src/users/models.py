from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _
from .managers import CustomUserManager
from xarala.utils import generate_key, upload_image_path


class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(_("email address"), unique=True)
    is_student = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)
    is_writer = models.BooleanField(default=False)
    phone = models.CharField(max_length=150, blank=True, null=True)
    address = models.CharField(max_length=250, blank=True, null=True)
    title = models.CharField(max_length=250, blank=True, null=True)
    facebook = models.CharField(max_length=250, blank=True, null=True)
    twitter = models.CharField(max_length=250, blank=True, null=True)
    linkedin = models.CharField(max_length=250, blank=True, null=True)
    github = models.CharField(max_length=250, blank=True, null=True)
    avatar = models.ImageField(upload_to=upload_image_path, null=True, blank=True)
    bio = models.TextField(blank=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email


class Experience(models.Model):
    user = models.ForeignKey(
        CustomUser, models.SET_NULL, null=True, blank=True, related_name="experiences"
    )
    begin_at = models.DateField(auto_now=False, blank=True, null=True)
    end_at = models.DateField(auto_now=False, blank=True, null=True)
    title = models.CharField(max_length=50, null=True, blank=True)
    Company = models.CharField(max_length=50, null=True, blank=True)
    project_link = models.URLField(max_length=50, null=True, blank=True)
    description = models.TextField()

    def __str__(self):
        return self.title


class Education(models.Model):
    user = models.ForeignKey(
        CustomUser, models.SET_NULL, null=True, blank=True, related_name="educations"
    )
    begin_at = models.DateField(auto_now=False, blank=True, null=True)
    end_at = models.DateField(auto_now=False, blank=True, null=True)
    title = models.CharField(max_length=50, null=True, blank=True)
    school = models.CharField(max_length=50, null=True, blank=True)
    description = models.TextField()

    def __str__(self):
        return self.title


class ResetCode(models.Model):
    code = models.CharField(max_length=4, unique=True)
    email = models.EmailField()
    expired = models.BooleanField(default=False)

    def _get_unique_label(self):
        unique_code = generate_key()
        while ResetCode.objects.filter(code=unique_code).exists():
            unique_code = generate_key()
        return unique_code

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = self._get_unique_code()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.code
