import graphene
from graphene_django import DjangoObjectType
from graphql.error.base import GraphQLError

from pages.models import Contact, Subscribe
from xarala.utils import SendSubscribeMail


class ContactType(DjangoObjectType):
    class Meta:
        model = Contact


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


class ContactUs(graphene.Mutation):
    contact = graphene.Field(ContactType)

    class Arguments:
        fullName = graphene.String()
        email = graphene.String()
        phone = graphene.String()
        message = graphene.String()

    def mutate(self, info, fullName, email, phone, message):
        contact = Contact(full_name=fullName, email=email, phone=phone, message=message)
        contact.save()
        return ContactUs(contact=contact)


class Mutation(graphene.ObjectType):
    subscribe_to_newsletter = CreateEmailSubscription.Field()
    contact_us = ContactUs.Field()
