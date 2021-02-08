import graphene
from django.conf import settings
from graphql import GraphQLError
from django.db.models import Q
from blog.tasks import author_submitted
from users.models import CustomUser
from users.schema import UserType

from xarala.utils import get_paginator, save_base_64
from .models import Post, Tag
from .query_types import PostType, TagType, PostPaginatedType


class Query(graphene.ObjectType):
    posts = graphene.Field(
        PostPaginatedType, search=graphene.String(), page=graphene.Int()
    )
    latestPosts = graphene.List(PostType, search=graphene.String())
    postsByAuthor = graphene.List(PostType, authorId=graphene.Int(required=True))
    post = graphene.Field(PostType, postSlug=graphene.String(), required=True)
    tags = graphene.List(TagType, search=graphene.String())
    tag = graphene.Field(TagType, tagName=graphene.String(required=True))
    postAuthors = graphene.List(UserType)

    def resolve_posts(self, info, page, search=None):
        page_size = 10
        if search:
            posts = Post.objects.search(search)
            return get_paginator(posts, page_size, page, PostPaginatedType)
        posts = Post.objects.published()
        return get_paginator(posts, page_size, page, PostPaginatedType)

    def resolve_latestPosts(self, info, search=None):
        if search:
            return Post.objects.search(search)
        return Post.objects.order_by("-id")[:3]

    def resolve_post(self, info, postSlug):
        post = Post.objects.get(slug=postSlug)
        return post

    def resolve_tags(self, info, search=None):
        if search:
            filter = Q(name__icontains=search) | Q(description__icontains=search)
            return Tag.objects.filter(filter)
        return Tag.objects.all()

    def resolve_tag(self, info, tagName):
        tag = Tag.objects.get(name=tagName)
        return tag

    def resolve_postsByAuthor(self, info, authorId):
        return Post.objects.by_author(authorId)

    def resolve_postAuthors(self, info):
        return CustomUser.objects.filter(is_writer=True)


# new product


class CreatePost(graphene.Mutation):
    post = graphene.Field(PostType)

    class Arguments:
        title = graphene.String()
        content = graphene.String()
        description = graphene.String()
        image = graphene.String()

    def mutate(self, info, title, content, description, image):
        user = info.context.user
        if user.is_anonymous:
            raise GraphQLError("Log in to add a post!")
        final_file_url = save_base_64(image)
        post = Post(title=title, content=content, description=description, author=user)
        post.image = final_file_url
        post.save()
        return CreatePost(post=post)


# update post


class UpdatePost(graphene.Mutation):
    post = graphene.Field(PostType)

    class Arguments:
        postId = graphene.Int(required=True)
        title = graphene.String()
        content = graphene.String()
        description = graphene.String()
        image = graphene.String()

    def mutate(self, info, postId, title, description, content, image=None):
        user = info.context.user
        post = Post.objects.get(id=postId)
        if user.is_anonymous or post.author != user:
            raise GraphQLError("Acces denied!")
        final_file_url = save_base_64(image) if image else post.image
        if post.author != user:
            raise GraphQLError("Not permited to update this post")
        post.title = title
        post.description = description
        post.image = final_file_url
        post.content = content
        post.save()
        return UpdatePost(post=post)


# delete post


class DeletePost(graphene.Mutation):
    postId = graphene.Int()

    class Arguments:
        postId = graphene.Int(required=True)

    def mutate(self, info, postId):
        user = info.context.user
        post = Post.objects.get(id=postId)
        if post.author != user:
            raise GraphQLError("Not permited to update this post")
        Post.objects.filter(id=postId).update(drafted=True)
        return DeletePost(postId=postId)


class SubmitPostToReview(graphene.Mutation):
    post = graphene.Field(PostType)

    class Arguments:
        postId = graphene.Int(required=True)

    def mutate(self, info, postId):
        user = info.context.user
        post = Post.objects.get(id=postId)
        if post.author != user:
            raise GraphQLError("Not permited to submit this post")
        post.submitted = True
        post.save()
        author_submitted.delay(
            post.author.email, post.title
        ) if not settings.DEBUG else None
        return SubmitPostToReview(post=post)


class Mutation(graphene.ObjectType):
    create_post = CreatePost.Field()
    update_post = UpdatePost.Field()
    delete_post = DeletePost.Field()
    submit_post_to_review = SubmitPostToReview.Field()
