from django import template

from course.models import Category

register = template.Library()


@register.simple_tag
def get_categories():
    categories = Category.objects.all()
    return categories
