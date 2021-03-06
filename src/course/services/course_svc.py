from django.db.models import Q
from course.models import Language


def get_languages(search=None):
    if search:
        filter = Q(name__icontains=search) | Q(abr__icontains=search)
        return Language.objects.filter(filter)
    return Language.objects.all()


def get_language_by_name(name):
    return Language.objects.get(name=name)
