"""Announcements admin."""

# Django
from django.contrib import admin

# Models
from apps.menu.models import Menu

# Third party integration
from import_export.admin import ImportExportModelAdmin
from superadmin.models import Menu as BaseMenu


@admin.register(Menu)
class MenuAdmin(ImportExportModelAdmin):
    """Page admin."""

    pass


@admin.register(BaseMenu)
class BaseMenuAdmin(ImportExportModelAdmin):
    """Page admin."""

    pass
