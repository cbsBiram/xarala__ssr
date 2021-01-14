import graphene
from graphql import GraphQLError
from django.db.models import Q
from .models import Post, Tag
from .query_types import PostType, TagType


class Query(graphene.ObjectType):
    posts = graphene.List(PostType, search=graphene.String())
    latestPosts = graphene.List(PostType, search=graphene.String())
    post = graphene.Field(PostType, postSlug=graphene.String(), required=True)
    tags = graphene.List(TagType, search=graphene.String())
    tag = graphene.Field(TagType, tagId=graphene.Int())

    def resolve_posts(self, info, search=None):
        if search:
            filter = Q(title__icontains=search) | Q(content__icontains=search)
            return Post.objects.filter(filter)
        return Post.objects.all()

    def resolve_latestPosts(self, info, search=None):
        if search:
            filter = Q(title__icontains=search) | Q(content__icontains=search)
            return Post.objects.filter(filter)
        return Post.objects.order_by('-id')[:3]

    def resolve_post(self, info, postSlug):
        post = Post.objects.get(slug=postSlug)
        return post

    def resolve_tags(self, info, search=None):
        if search:
            filter = Q(name__icontains=search) | Q(description__icontains=search)
            return Tag.objects.filter(filter)
        return Tag.objects.all()

    def resolve_tag(self, info, tagId):
        tag = Tag.objects.get(pk=tagId)
        return tag


# new product


class CreatePost(graphene.Mutation):
    post = graphene.Field(PostType)

    class Arguments:
        title = graphene.String()
        content = graphene.Int()
        image = graphene.String()

    def mutate(self, info, title, content, image):
        user = info.context.user
        if user.is_anonymous:
            raise GraphQLError("Log in to add a post!")

        post = Post(title=title, content=content, image=image, author=user)
        post.save()
        return CreatePost(post=post)


# update post


class UpdatePost(graphene.Mutation):
    post = graphene.Field(PostType)

    class Arguments:
        postId = graphene.Int(required=True)
        title = graphene.String()
        content = graphene.Int()
        image = graphene.String()

    def mutate(self, info, postId, title, description, image):
        user = info.context.user
        if user.is_anonymous:
            raise GraphQLError("Log in to edit a post!")
        post = Post.objects.get(id=postId)
        if post.author != user:
            raise GraphQLError("Not permited to update this post")
        post.title = title
        post.description = description
        post.image = image
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


class Mutation(graphene.ObjectType):
    create_post = CreatePost.Field()
    update_post = UpdatePost.Field()
    delete_post = DeletePost.Field()
