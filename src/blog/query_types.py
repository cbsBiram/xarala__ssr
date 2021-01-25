import graphene
from graphene_django import DjangoObjectType
from .models import Post, Tag


class PostType(DjangoObjectType):
    class Meta:
        model = Post


class TagType(DjangoObjectType):
    class Meta:
        model = Tag


class PostPaginatedType(graphene.ObjectType):
    page = graphene.Int()
    pages = graphene.Int()
    has_next = graphene.Boolean()
    has_prev = graphene.Boolean()
    objects = graphene.List(PostType)