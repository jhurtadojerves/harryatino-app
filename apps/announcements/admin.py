"""Announcements admin."""

# Django
from django.contrib import admin

# Third party integration
from import_export.admin import ImportExportModelAdmin

# Models
from apps.announcements.models import Announcement


@admin.register(Announcement)
class AnnouncementAdmin(ImportExportModelAdmin):
    """Announcement admin."""

    list_display = ("id", "name")
