""" Audit model admin """

# Django
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from import_export.admin import ImportExportModelAdmin
from django.utils.translation import gettext_lazy as _


# Models
from apps.authentication.models import User


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
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
