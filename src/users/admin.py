from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from import_export import resources
from import_export.admin import ImportExportModelAdmin

from users.services.user_svc import export_to_csv

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser, Experience, ResetCode


class CustomUserResource(resources.ModelResource):
    class Meta:
        model = CustomUser
        exclude = "password"


class CustomUserAdmin(UserAdmin, ImportExportModelAdmin):
    resource_class = CustomUserResource
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = (
        "email",
        "is_staff",
        "is_active",
        "is_student",
        "is_teacher",
    )
    list_filter = (
        "is_staff",
        "is_active",
        "is_student",
        "is_teacher",
    )
    list_editable = (
        "is_active",
        "is_student",
        "is_teacher",
    )
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "email",
                    "password",
                    "avatar",
                    "bio",
                    "first_name",
                    "last_name",
                )
            },
        ),
        ("Permissions", {"fields": ("is_staff", "is_active")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "password1", "password2", "is_staff", "is_active"),
            },
        ),
    )
    search_fields = ("email",)
    ordering = ("email",)
    actions = [export_to_csv]


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Experience)
admin.site.register(ResetCode)