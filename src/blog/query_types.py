import graphene
from graphene_django import DjangoObjectType
from .models import Post, Tag


class PostType(DjangoObjectType):
    class Meta:
        model = Post

    get_previous = graphene.Field(graphene.String)
    get_next = graphene.Field(graphene.String)

    def resolve_get_previous(instance, info, **kwargs):
        return instance.previous()

    def resolve_get_next(instance, info, **kwargs):
        return instance.next()


class TagType(DjangoObjectType):
    class Meta:
        model = Tag

    get_tag_posts = graphene.List(PostType)

    def resolve_get_tag_posts(instance, info, **kwargs):
        return instance.tag_posts()


class PostPaginatedType(graphene.ObjectType):
    page = graphene.Int()
    pages = graphene.Int()
    has_next = graphene.Boolean()
    has_prev = graphene.Boolean()
    objects = graphene.List(PostType)