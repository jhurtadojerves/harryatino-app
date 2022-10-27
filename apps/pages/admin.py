"""Announcements admin."""

# Django
from django.contrib import admin

# Third party integration
from import_export.admin import ImportExportModelAdmin

# Models
from apps.pages.models import Page


@admin.register(Page)
class PageAdmin(ImportExportModelAdmin):
    """Page admin."""

    list_display = ("id", "name", "show_in_home_page", "slug")
