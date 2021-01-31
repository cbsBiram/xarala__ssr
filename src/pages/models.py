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
    image = models.ImageField(upload_to=upload_image_path, null=True, blank=True)
    active = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class Contact(models.Model):
    full_name = models.CharField(max_length=150)
    email = models.EmailField(max_length=150)
    phone = models.CharField(max_length=150)
    rule = models.CharField(max_length=150, blank=True, null=True)
    enterprise = models.CharField(max_length=150, blank=True, null=True)
    message = models.TextField(blank=True)

    def __str__(self):
        return f"{self.full_name} : {self.email} - {self.phone}"


class Team(models.Model):
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=150)
    phone = models.CharField(max_length=150)
    profession = models.CharField(max_length=150)
    profile = models.ImageField(upload_to=upload_image_path, blank=True, null=True)
    bio = models.TextField()
    website = models.URLField(max_length=150, blank=True, null=True)
    facebook = models.URLField(max_length=150, blank=True, null=True)
    twitter = models.URLField(max_length=150, blank=True, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
