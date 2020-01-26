from django.db import models


class Help(models.Model):
    name = models.CharField(max_length=150)
    summary = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.name


class Technology(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class MentorShipType(models.Model):
    name = models.CharField(max_length=150)
    summary = models.CharField(max_length=150)
    icon = models.CharField(max_length=150, null=True, blank=True)
    duration = models.IntegerField(default=15)  # duration per minute
    budget = models.DecimalField(default=0, max_digits=13, decimal_places=2)


class MentorShip(models.Model):
    # student
    # tutor
    pass
