from django import forms
from django.forms import BaseForm
from django.forms.forms import DeclarativeFieldsMetaclass
from django_select2.forms import ModelSelect2Widget, Select2Widget
from superadmin.forms import ModelForm

from apps.dynamicforms.models import Field, Fieldset, Form
from apps.dynamicforms.utils import FieldDynamic, get_type_and_widget


class BaseForm(BaseForm, metaclass=DeclarativeFieldsMetaclass):
    def parse(self, fieldset):
        def wrap(fields):
            fields = fields if isinstance(fields, (list, tuple)) else [fields]
            return {
                "bs_cols": int(12 / len(fields)),
                "fields": [self[field] for field in fields],
            }

        fieldset_list = list(map(wrap, fieldset))
        return fieldset_list

    def get_fieldsets(self):
        fieldsets_list = self.fieldsets
        fieldsets = (
            [(None, fieldsets_list)]
            if isinstance(fieldsets_list, (list, tuple))
            else fieldsets_list.items()
        )
        fieldsets = [
            {"title": title or "", "fieldset": self.parse(fieldset)}
            for title, fieldset in fieldsets
        ]

        return fieldsets

    def has_fieldsets(self):
        return hasattr(self, "fieldsets")


class CreationDynamicForm(BaseForm):
    def __init__(self, *args, **kwargs):
        self.form = kwargs.pop("form", None)
        disable_fields = kwargs.pop("disable_fields", False)
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
                    disabled=disable_fields,
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
                search_fields=[
                    "name__unaccent__icontains",
                    "description__unaccent__icontains",
                ],
                attrs={
                    "data-minimum-input-length": 0,
                    "data-app": "dynamicforms",
                    "data-model": "Form",
                },
            ),
            "fieldset": ModelSelect2Widget(
                model=Fieldset,
                search_fields=["name__unaccent__icontains"],
                attrs={
                    "data-minimum-input-length": 0,
                    "data-app": "dynamicforms",
                    "data-model": "Fieldset",
                },
            ),
            "type": Select2Widget(
                attrs={"data-minimum-input-length": 0},
            ),
        }


class FieldLineForm(FieldForm):
    """Class define form the field in formsets"""

    class Meta(FieldForm.Meta):
        """Class Information"""

        # TODO: CHECK EXCLUDE
        # FieldForm.Meta.exclude = ("name",)
        widgets = FieldForm.Meta.widgets
        widgets.update(
            {
                "widget": forms.Textarea(attrs={"rows": 3}),
            }
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
