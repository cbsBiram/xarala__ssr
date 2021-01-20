import graphene
import graphql_jwt
from django.conf import settings
from django.contrib.auth.forms import PasswordChangeForm
from django.db.models import Q
from graphene_django import DjangoObjectType
from graphene_django.forms.mutation import DjangoFormMutation
from graphql import GraphQLError

from xarala.utils import email_validation_function

from .models import CustomUser as User
from .models import ResetCode
from .tasks import account_created, send_password_reset_email


class UserType(DjangoObjectType):
    class Meta:
        model = User


class UpdateUser(graphene.Mutation):
    user = graphene.Field(UserType)

    class Arguments:
        userId = graphene.Int(required=True)
        firstName = graphene.String()
        lastName = graphene.String()
        phone = graphene.String()
        address = graphene.String()

    def mutate(self, info, userId, firstName, lastName, phone, address):
        user = info.context.user
        if user.is_anonymous:
            raise GraphQLError("Log in to edit user account!")
        user = User.objects.get(id=userId)
        user.first_name = firstName
        user.last_name = lastName
        user.address = address
        user.phone = phone
        user.save()
        return UpdateUser(user=user)


class AuthMutation(graphene.ObjectType):

    # django-graphql-jwt inheritances
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()
    revoke_token = graphql_jwt.Revoke.Field()


class Query(graphene.ObjectType):
    me = graphene.Field(UserType)
    user = graphene.Field(UserType, id=graphene.Int(required=True))

    def resolve_user(self, info, id):
        return User.objects.get(id=id)

    def resolve_me(self, info):
        user = info.context.user
        if user.is_anonymous:
            raise GraphQLError("Not loged in!")
        return user


class RegisterUser(graphene.Mutation):
    user = graphene.Field(UserType)

    class Arguments:
        email = graphene.String(required=True)
        password = graphene.String(required=True)

    def mutate(self, info, email, password):
        mail_to_lower = email_validation_function(email.lower())
        user = User(email=mail_to_lower)
        user.set_password(password)
        user.is_student = True
        user.save()
        account_created.delay(mail_to_lower) if not settings.DEBUG else None
        return RegisterUser(user)


class PasswordResetEmail(graphene.Mutation):
    user = graphene.Field(UserType)

    class Arguments:
        email = graphene.String(required=True)

    def mutate(self, info, email):
        mail_to_lower = email_validation_function(email.lower())
        user = ""
        try:
            user = User.objects.get(email=mail_to_lower)
        except User.DoesNotExist:
            raise GraphQLError(
                "Compte non trouvé, merci de bien vérifier votre adresse email"
            )
        send_password_reset_email.delay(mail_to_lower)
        return PasswordResetEmail(user)


class PasswordReset(graphene.Mutation):
    user = graphene.Field(UserType)

    class Arguments:
        email = graphene.String(required=True)
        code = graphene.String(required=True)
        newPassword = graphene.String(required=True)

    def mutate(self, info, email, code, newPassword):
        mail_to_lower = email_validation_function(email.lower())
        reset_code = ResetCode.objects.filter(
            Q(code=code) & Q(email=mail_to_lower) & Q(expired=False)
        ).exists()
        if reset_code:
            try:
                user = User.objects.get(email=mail_to_lower)
                user.set_password(newPassword)
                user.save()
            except User.DoesNotExist:
                raise GraphQLError(
                    "Compte non trouvé, merci de bien vérifier votre adresse email"
                )
        else:
            raise GraphQLError("Code non trouvé dans notre système")
        ResetCode.objects.filter(code=code).update(expired=True)
        user = User.objects.get(email=mail_to_lower)
        return PasswordReset(user)


class PasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super().__init__(user, *args, **kwargs)


class ChangePassword(DjangoFormMutation):
    class Meta:
        form_class = PasswordChangeForm

    @classmethod
    def get_form_kwargs(cls, root, info, **mutation_input):
        return {
            **super().get_form_kwargs(root, info, **mutation_input),
            "user": info.context.user,
        }


class Mutation(AuthMutation, graphene.ObjectType):
    update_user = UpdateUser.Field()
    register = RegisterUser.Field()
    send_password_reset_email = PasswordResetEmail.Field()
    reset_password = PasswordReset.Field()
    change_password = ChangePassword.Field()


schema = graphene.Schema(query=Query)
