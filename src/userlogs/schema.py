import graphene
from django.db.models import Q
from graphene_django import DjangoObjectType
from graphql import GraphQLError

from .models import UserLog
from xarala.utils import get_paginator


class UserLogType(DjangoObjectType):
    class Meta:
        model = UserLog


class UserLogPaginatedType(graphene.ObjectType):
    page = graphene.Int()
    pages = graphene.Int()
    has_next = graphene.Boolean()
    has_prev = graphene.Boolean()
    objects = graphene.List(UserLogType)


class Query(graphene.ObjectType):
    usersLogs = graphene.Field(UserLogPaginatedType, page=graphene.Int(required=True))

    def resolve_usersLogs(self, info, page):
        page_size = 10
        user = info.context.user
        if not user.is_staff:
            raise GraphQLError("You're not an admin!")
        users_logs = UserLog.objects.order_by("-id")
        return get_paginator(users_logs, page_size, page, UserLogPaginatedType)


schema = graphene.Schema(query=Query)
