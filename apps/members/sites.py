'''
# Third party integration
from superadmin.decorators import register

# Local
from config.base import BaseSite
from .forms import FieldForm, FormForm, FieldLineFormset


@register("procedures.Field")
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


@register("procedures.Fieldset")
class FieldsetSite(BaseSite):
    """Site from Fieldset"""

    fields = ("name",)
    list_fields = ("name",)
    detail_fields = ("name",)


@register("procedures.Form")
class FormSite(BaseSite):
    """Site from Form"""

    form_class = FormForm
    inlines = {"lines": FieldLineFormset}

    form_template_name = None
    list_fields = ("code", "name", "description")
    detail_fields = ("code", "name", "description")
'''
