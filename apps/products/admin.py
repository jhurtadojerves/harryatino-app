"""Products app admin."""

# Django
from django.contrib import admin

# Third party integration
from import_export.admin import ImportExportModelAdmin

# Models
from apps.products.models import Product, Category, Section


@admin.register(Product)
class ProductAdmin(ImportExportModelAdmin):
    """Product admin."""

    list_display = (
        "number",
        "reference",
        "name",
        "points",
        "cost",
        "initial_stock",
        "description",
        "check_stock",
        "slug",
    )

    list_filter = ("category",)
    search_fields = ("reference", "name", "category__name", "id")
    autocomplete_fields = ("category",)


@admin.register(Category)
class CategoryAdmin(ImportExportModelAdmin):
    """Category admin. """

    list_display = ("name", "section")
    search_fields = ("name",)
    list_filter = ("section",)
    autocomplete_fields = ("section",)


@admin.register(Section)
class SectionAdmin(ImportExportModelAdmin):
    """Section admin. """

    list_display = ("name",)
    search_fields = ("name",)
