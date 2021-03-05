from django.db import models
from django.db.models import Q


class LearningPathQuerySet(models.QuerySet):
    def published(self):
        return self.filter(published=True)

    def unpublished(self):
        return self.filter(published=False)

    def search(self, query):
        lookup = (
            Q(title__icontains=query)
            | Q(description__icontains=query)
            | Q(slug__icontains=query)
        )

        return self.filter(lookup)


class LearningPathManager(models.Manager):
    def get_queryset(self):
        return LearningPathQuerySet(self.model, using=self._db)

    def published(self):
        return self.get_queryset().published()

    def unpublished(self):
        return self.get_queryset().unpublished()

    def search(self, query=None):
        if query is None:
            return self.get_queryset().none()
        return self.get_queryset().published().search(query)
