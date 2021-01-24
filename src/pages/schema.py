import graphene
from graphql.error.base import GraphQLError
from pages.models import Subscribe
from xarala.utils import SendSubscribeMail


class CreateEmailSubscription(graphene.Mutation):
    subscribed = graphene.Boolean()

    class Arguments:
        email = graphene.String()

    def mutate(self, info, email):
        subscribed = False
        email_qs = Subscribe.objects.filter(email_id=email)
        if email_qs.exists():
            raise GraphQLError("You've already subscribed")
        else:
            Subscribe.objects.create(email_id=email)
            SendSubscribeMail(email)
            subscribed = True
        return CreateEmailSubscription(subscribed)


class Mutation(graphene.ObjectType):
    subscribe_to_newsletter = CreateEmailSubscription.Field()
