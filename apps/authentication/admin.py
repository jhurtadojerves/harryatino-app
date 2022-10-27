""" Audit model admin """

# Django
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from import_export.admin import ImportExportModelAdmin

# Models
from apps.authentication.models import User


@admin.action(description="Disable selected users")
def disable_users(modeladmin, request, queryset):
    queryset.update(
        is_active=False, is_staff=False, is_superuser=False, is_moderator=False
    )


@admin.register(User)
class CustomUserAdmin(ImportExportModelAdmin, UserAdmin):
    """User model admin"""

    list_display = list()
    for item in UserAdmin.list_display:
        list_display.append(item)
    list_display.append("old_number")

    fieldsets = (
        (None, {"fields": ("username", "password", "old_number")}),
        (_("Personal info"), {"fields": ("first_name", "last_name", "email")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "is_moderator",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    actions = [disable_users]
