"""Sales admin."""

# Django
from django.contrib import admin

# Models
from apps.sales.models import Sale

# Third Party Integration
from import_export.admin import ImportExportModelAdmin


@admin.register(Sale)
class SaleAdmin(ImportExportModelAdmin):
    """Sale model admin."""

    list_display = ("product", "date", "profile")
    search_fields = (
        "product__name",
        "product__reference",
        "profile__nick",
        "profile__forum_user_id",
    )
    autocomplete_fields = ("product", "profile")
