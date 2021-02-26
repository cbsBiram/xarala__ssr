from django.utils import timezone
from django.db import models
from django.db.models import Q


class CourseQuerySet(models.QuerySet):
    def published(self):
        now = timezone.now()
        return self.filter(publish_date__lte=now)

    def unpublished(self):
        return self.filter(published=False, submitted=True)

    def search(self, query):
        lookup = (
            Q(title__icontains=query)
            | Q(description__icontains=query)
            | Q(slug__icontains=query)
            | Q(teacher__first_name__icontains=query)
            | Q(teacher__last_name__icontains=query)
            | Q(teacher__email__icontains=query)
        )

        return self.filter(lookup)


class CourseManager(models.Manager):
    def get_queryset(self):
        return CourseQuerySet(self.model, using=self._db)

    def published(self):
        return self.get_queryset().published()

    def unpublished(self):
        return self.get_queryset().unpublished()

    def search(self, query=None):
        if query is None:
            return self.get_queryset().none()
        return self.get_queryset().published().search(query)


class LessonQuerySet(models.QuerySet):
    def search(self, query):
        lookup = (
            Q(title__icontains=query)
            | Q(text__icontains=query)
            | Q(slug__icontains=query)
        )

        return self.filter(lookup)


class LessonManager(models.Manager):
    def get_queryset(self):
        return LessonQuerySet(self.model, using=self._db)

    # def published(self):
    #     return self.get_queryset()

    def search(self, query=None):
        if query is None:
            return self.get_queryset().none()
        return self.get_queryset().search(query)
