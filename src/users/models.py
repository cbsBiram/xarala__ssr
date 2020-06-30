from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _
from .managers import CustomUserManager
from xarala.utils import upload_image_path


class Social(models.Model):
    # facebook
    facebook = models.CharField(max_length=150, null=True, blank=True)
    # twitter
    twitter = models.CharField(max_length=150, null=True, blank=True)
    # instagram
    instagram = models.CharField(max_length=150, null=True, blank=True)
    # github
    github = models.CharField(max_length=150, null=True, blank=True)
    # siteweb
    website = models.CharField(max_length=150, null=True, blank=True)
    # linkedin
    linkedin = models.CharField(max_length=150, null=True, blank=True)
    # stack
    stackoverflow = models.CharField(max_length=150, null=True, blank=True)
    # whatsapp
    whatsapp = models.CharField(max_length=150, null=True, blank=True)


class CustomUser(AbstractUser):
    STUDENT = "ST"
    TEACHER = "TC"
    MENTOR = "MT"
    WRITER = "WT"
    USERTYPE = [
        (STUDENT, "Student"),
        (TEACHER, "Teacher"),
        (MENTOR, "Mentor"),
        (WRITER, "Writer"),
    ]
    username = None
    email = models.EmailField(_("email address"), unique=True)
    is_student = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)
    scoial = models.ForeignKey(Social, models.SET_NULL, null=True, blank=True)
    phone = models.CharField(max_length=150, blank=True, null=True)
    address = models.CharField(max_length=250, blank=True, null=True)
    avatar = models.ImageField(upload_to=upload_image_path, null=True, blank=True)
    bio = models.TextField(blank=True)
    user_type = models.CharField(
        max_length=10, choices=USERTYPE, default=STUDENT, null=True
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email
