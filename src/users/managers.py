from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import ugettext_lazy as _


class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """

    def create_user(self, email, password=None, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError(_("The Email must be set"))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))
        return self.create_user(email, password, **extra_fields)

    def teachers(self):
        return self.get_queryset().filter(is_teacher=True)

    def valid_teachers(self):
        return self.get_queryset().filter(
            is_teacher=True, courses_created__count__gte=1
        )

    def invalid_teachers(self):
        return self.get_queryset().filter(is_teacher=True, courses_created__count=0)

    def students(self):
        return self.get_queryset().filter(is_student=True)

    def no_enrolled_students(self):
        return self.get_queryset().filter(is_student=True, courses_enrolled__count=0)

    def enrolled_students(self):
        return self.get_queryset().filter(
            is_student=True, courses_enrolled__count__gte=1
        )
