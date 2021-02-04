import graphene
import graphql_jwt
from django.conf import settings
from django.contrib.auth.forms import PasswordChangeForm

from django.db.models import Q
from graphene_django import DjangoObjectType
from graphene_django.forms.mutation import DjangoFormMutation
from graphql import GraphQLError
from blog.query_types import PostType
from users.upload import save_base_64


from xarala.utils import email_validation_function, save_base_64

from .models import CustomUser as User
from .models import ResetCode
from .tasks import account_created, send_password_reset_email


class UserType(DjangoObjectType):
    class Meta:
        model = User

    get_user_posts = graphene.List(PostType)

    def resolve_get_user_posts(instance, info, **kwargs):
        return instance.user_posts()


class UpdateUser(graphene.Mutation):
    user = graphene.Field(UserType)

    class Arguments:
        firstName = graphene.String()
        lastName = graphene.String()
        phone = graphene.String()
        address = graphene.String()
        bio = graphene.String()

    def mutate(self, info, firstName, lastName, phone, address, bio):
        user = info.context.user
        if user.is_anonymous:
            raise GraphQLError("Log in to edit user account!")
        user = User.objects.get(id=user.id)
        user.first_name = firstName
        user.last_name = lastName
        user.address = address
        user.phone = phone
        user.bio = bio
        user.save()
        return UpdateUser(user=user)


class UpdateAvatar(graphene.Mutation):
    success = graphene.Boolean()

    class Arguments:
        file = graphene.String()

    def mutate(self, info, file):
        final_file_url = save_base_64(file)
        user = info.context.user
        if user.is_anonymous:
            raise GraphQLError("Log in to edit user account!")
        user.avatar = final_file_url
        user.save()
        return UpdateAvatar(success=True)


class AuthMutation(graphene.ObjectType):

    # django-graphql-jwt inheritances
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()
    revoke_token = graphql_jwt.Revoke.Field()


class Query(graphene.ObjectType):
    me = graphene.Field(UserType)
    user = graphene.Field(UserType, id=graphene.Int(required=True))
    users = graphene.List(UserType)
    students = graphene.List(UserType)
    teachers = graphene.List(UserType)
    authors = graphene.List(UserType)

    def resolve_user(self, info, id):
        return User.objects.get(id=id)

    def resolve_me(self, info):
        user = info.context.user
        if user.is_anonymous:
            raise GraphQLError("Not loged in!")
        return user

    def resolve_users(self, info):
        user = info.context.user
        if not user.is_staff:
            raise GraphQLError("You're not admin!")
        return User.objects.all()

    def resolve_students(self, info):
        user = info.context.user
        if not user.is_staff:
            raise GraphQLError("You're not admin!")
        return User.objects.filter(is_student=True)

    def resolve_teachers(self, info):
        user = info.context.user
        if not user.is_staff:
            raise GraphQLError("You're not admin!")
        return User.objects.filter(is_teacher=True)

    def resolve_authors(self, info):
        user = info.context.user
        if not user.is_staff:
            raise GraphQLError("You're not admin!")
        return User.objects.filter(is_writer=True)


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
        send_password_reset_email.delay(mail_to_lower) if not settings.DEBUG else None
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
    update_avatar = UpdateAvatar.Field()
    register = RegisterUser.Field()
    send_password_reset_email = PasswordResetEmail.Field()
    reset_password = PasswordReset.Field()
    change_password = ChangePassword.Field()


schema = graphene.Schema(query=Query)
