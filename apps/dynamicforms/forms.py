from django import forms
from django.forms import BaseForm
from django.forms.forms import DeclarativeFieldsMetaclass
from django_select2.forms import ModelSelect2Widget, Select2Widget
from superadmin.forms import ModelForm

from apps.dynamicforms.models import Field, Form, Fieldset
from apps.dynamicforms.utils import FieldDynamic, get_type_and_widget
from django.utils.text import slugify


class BaseForm(BaseForm, metaclass=DeclarativeFieldsMetaclass):
    def get_fieldsets(self):
        sets = list()
        for fieldset in self.fieldsets:
            if isinstance(fieldset, tuple):
                sets.append(
                    {
                        "bs_cols": int(12 / len(fieldset)),
                        "fields": [self[field] for field in fieldset],
                    }
                )
            else:
                sets.append({"bs_cols": 12, "fields": [self[fieldset]]})
        return sets

    def has_fieldsets(self):
        return hasattr(self, "fieldsets")


class CreationDynamicForm(BaseForm):
    def __init__(self, *args, **kwargs):
        self.form = kwargs.pop("form", None)
        super().__init__(*args, **kwargs)
        if self.form:
            all_fields = self.form.field_form.all().order_by("pk")
            for field in all_fields:
                class_type, class_widget = get_type_and_widget(field.type)
                field_class = FieldDynamic(
                    label=field.label,
                    required=field.required,
                    attrs_widget=field.widget,
                    class_type=class_type,
                    class_widget=class_widget,
                )
                self.fields[f"{field.name}"] = field_class.create_field
            self.fieldsets = self.form.get_fieldsets

    def save(self):
        return self.cleaned_data


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
                attrs={
                    "data-minimum-input-length": 0,
                    "data-app": "dynamicforms",
                    "data-model": "Form",
                },
            ),
            "fieldset": ModelSelect2Widget(
                model=Fieldset,
                search_fields=["name__icontains"],
                attrs={
                    "data-minimum-input-length": 0,
                    "data-app": "dynamicforms",
                    "data-model": "Fieldset",
                },
            ),
            "type": Select2Widget(attrs={"data-minimum-input-length": 0},),
        }


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


class FormForm(ModelForm):
    """Class define form the Form"""

    class Meta:
        """Class information"""

        model = Form
        fieldsets = (
            "name",
            "description",
        )
        widgets = {"description": forms.Textarea(attrs={"rows": 3})}


"""
choices=(("Teléfono", "Teléfono"),("Alcantarillado", "Alcantarillado"),("Energía eléctrica", "Energía eléctrica"),("Agua potable", "Agua potable"),("Barrido de calles", "Barrido de calles"),("Recolección de basura", "Recolección de basura"))
"""
