"""Announcements admin."""

# Django
from django.contrib import admin

# Third party integration
from import_export.admin import ImportExportModelAdmin
from superadmin.models import Menu as BaseMenu

# Models
from apps.menu.models import Menu


@admin.register(Menu)
class MenuAdmin(ImportExportModelAdmin):
    """Page admin."""

    pass


@admin.register(BaseMenu)
class BaseMenuAdmin(ImportExportModelAdmin):
    """Page admin."""

    pass
