"""Procedures sites"""

# Third party integration
from superadmin.decorators import register

# Base
from apps.dynamicforms.forms import FieldForm, FormForm
from apps.dynamicforms.formsets import FieldLineFormset
from config.base import BaseSite


@register("dynamicforms.Field")
class FieldSite(BaseSite):
    """Site from Field"""

    form_class = FieldForm
    list_fields = ("form", "fieldset", "label")
    detail_fields = (
        "form",
        "fieldset",
        "type",
        "label",
        "name",
        "widget",
        "required",
    )


@register("dynamicforms.Fieldset")
class FieldsetSite(BaseSite):
    """Site from Fieldset"""

    fields = ("name",)
    list_fields = ("name",)
    detail_fields = ("name",)


@register("dynamicforms.Form")
class FormSite(BaseSite):
    """Site from Form"""

    form_class = FormForm
    inlines = {"lines": FieldLineFormset}
    form_template_name = None
    list_fields = ("name", "description")
    detail_fields = ("name", "description")


@register("dynamicforms.Action")
class ActionSite(BaseSite):
    detail_template_name = None
    list_fields = ("name",)
    detail_fields = ("name",)


@register("dynamicforms.AuditAPI")
class AuditAPISite(BaseSite):
    """Site to audit api"""

    list_fields = ("username", "action", "created_date")
    detail_fields = list_fields
    detail_template_name = None
