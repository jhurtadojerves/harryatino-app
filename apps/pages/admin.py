"""Announcements admin."""

# Django
from django.contrib import admin

# Models
from apps.pages.models import Page

# Third party integration
from import_export.admin import ImportExportModelAdmin


@admin.register(Page)
class PageAdmin(ImportExportModelAdmin):
    """Page admin."""

    list_display = ("id", "name", "show_in_home_page", "slug")
