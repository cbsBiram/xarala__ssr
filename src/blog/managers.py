from django.utils import timezone
from django.db import models
from django.db.models import Q


class BlogPostQuerySet(models.QuerySet):
    def published(self):
        now = timezone.now()
        return self.filter(publish_date__lte=now, drafted=False)

    def search(self, query):
        lookup = (
            Q(title__icontains=query)
            | Q(content__icontains=query)
            | Q(slug__icontains=query)
            | Q(author__first_name__icontains=query)
            | Q(author__last_name__icontains=query)
            | Q(author__email__icontains=query)
        )

        return self.filter(lookup)


class BlogPostManager(models.Manager):
    def get_queryset(self):
        return BlogPostQuerySet(self.model, using=self._db)

    def published(self):
        return self.get_queryset().published()

    def search(self, query=None):
        if query is None:
            return self.get_queryset().none()
        return self.get_queryset().published().search(query)

    def by_author(self, author_id):
        return self.get_queryset().published().filter(author__id=author_id)
