import graphene
from graphene_django import DjangoObjectType
from graphql import GraphQLError
from .models import CustomUser


class CustomUserType(DjangoObjectType):
    class Meta:
        model = CustomUser


class Query(graphene.ObjectType):
    user = graphene.Field(CustomUserType, id=graphene.Int(required=True))
    me = graphene.Field(CustomUserType)

    def resolve_user(self, info, id):
        return CustomUser.objects.get(id=id)

    def resolve_me(self, info):
        user = info.context.user
        if user.is_anonymous:
            raise GraphQLError("Not loged in!")
        return user


class CreateUser(graphene.Mutation):
    user = graphene.Field(CustomUserType)

    class Arguments:
        phone = graphene.String(required=True)
        password = graphene.String(required=True)

    def mutate(self, info, phone, password):
        user = CustomUser(phone=phone)
        user.set_password(password)
        user.save()
        return CreateUser(user)


class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()
