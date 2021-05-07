"""Dynamic forms app admin."""

# Django
from django.contrib import admin

# Third party integration
from import_export.admin import ImportExportModelAdmin

# Models
from apps.dynamicforms.models import Fieldset, Field, Form


@admin.register(Fieldset)
class FieldsetAdmin(ImportExportModelAdmin):
    """Fieldset admin."""


@admin.register(Field)
class FieldAdmin(ImportExportModelAdmin):
    """Field admin. """


@admin.register(Form)
class FormAdmin(ImportExportModelAdmin):
    """Form admin. """
