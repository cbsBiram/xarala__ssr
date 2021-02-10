import graphene
from django.db.models import Q
from graphql import GraphQLError
from itertools import chain

from blog.query_types import PostType
from blog.models import Post
from course.query_types import CourseType
from course.models import Course


class SearchResultType(graphene.Union):
    class Meta:
        types = (CourseType, PostType)


class Query(graphene.ObjectType):
    homepageSearch = graphene.List(SearchResultType, query=graphene.String())

    def resolve_homepageSearch(self, info, query):
        if query:
            post_results = Post.objects.search(query)
            course_results = Course.objects.search(query)
            queryset_chain = chain(post_results, course_results)
            qs = sorted(queryset_chain, key=lambda instance: instance.pk, reverse=True)
            return qs
        return Post.objects.none()


schema = graphene.Schema(query=Query)
