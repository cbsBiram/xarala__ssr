from graphene_django import DjangoObjectType
from .models import Post, Tag


class PostType(DjangoObjectType):
    class Meta:
        model = Post


class TagType(DjangoObjectType):
    class Meta:
        model = Tag
