"""Announcements admin."""

# Django
from django.contrib import admin

# Models
from apps.announcements.models import Announcement

# Third party integration
from import_export.admin import ImportExportModelAdmin


@admin.register(Announcement)
class AnnouncementAdmin(ImportExportModelAdmin):
    """Announcement admin."""

    list_display = ("id", "name")
