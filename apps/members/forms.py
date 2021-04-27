"""Forms for member module"""

# Django
from django import forms
from django.forms import inlineformset_factory

# Third Party Integration

from django_select2.forms import (
    ModelSelect2Widget,
    Select2Widget,
)
from superadmin.forms import ModelForm

from apps.members.models import (
    Field,
    Form,
    Fieldset,
)


class FieldForm(ModelForm):
    """Class define form the field"""

    class Meta:
        """Class information"""

        model = Field
        fieldsets = (
            ("form", "fieldset"),
            ("type", "label", "name", "required"),
            ("widget",),
        )
        widgets = {
            "form": ModelSelect2Widget(
                model=Form,
                search_fields=["name__icontains", "description__icontains"],
                attrs={"data-minimum-input-length": 0,},
            ),
            "fieldset": ModelSelect2Widget(
                model=Fieldset,
                search_fields=["name__icontains"],
                attrs={"data-minimum-input-length": 0,},
            ),
            "type": Select2Widget(attrs={"data-minimum-input-length": 0},),
        }


class FormForm(ModelForm):
    """Class define form the Form"""

    class Meta:
        """Class information"""

        model = Form
        fieldsets = (("code", "name"), ("description",))
        widgets = {"description": forms.Textarea(attrs={"rows": 3})}


class FieldLineForm(FieldForm):
    """Class define form the field in formsets"""

    class Meta(FieldForm.Meta):
        """Class Information"""

        # TODO: CHECK EXCLUDE
        # FieldForm.Meta.exclude = ("name",)
        widgets = FieldForm.Meta.widgets
        widgets.update(
            {"widget": forms.Textarea(attrs={"rows": 3}),}
        )


FieldLineFormset = inlineformset_factory(
    Form, Field, form=FieldLineForm, min_num=0, validate_min=False,
)
