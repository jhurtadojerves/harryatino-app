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

    list_display = ("product", "date", "profile", "buyer")
    search_fields = (
        "product__name",
        "product__reference",
        "profile__nick",
        "profile__forum_user_id",
    )
    list_filter = ("buyer",)
    autocomplete_fields = ("product", "profile")
