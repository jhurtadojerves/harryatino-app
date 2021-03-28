"""Products form"""

# Django
from django import forms

# Third party integration
from django_select2.forms import (
    ModelSelect2Widget,
    Select2Widget,
)
from superadmin.forms import ModelForm

# Local
from apps.products.models import Product, Section


class SorterSettingsForm(ModelForm):
    section = forms.ModelChoiceField(
        label="Sección",
        queryset=Section.objects.all(),
        widget=ModelSelect2Widget(
            model="product.Section",
            search_fields=["name__icontains",],
            max_results=100,
            attrs={"data-minimum-input-length": 0,},
        ),
    )

    class Meta:
        model = Product
        fieldsets = (
            ("name", "reference",),
            ("points", "cost"),
            ("initial_stock", "image"),
            ("section", "category",),
            ("description",),
        )
        widgets = {
            "category": ModelSelect2Widget(
                model="products.Category",
                search_fields=["name__icontains"],
                dependent_fields={"section": "section"},
                attrs={"data-minimum-input-length": 0,},
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.id:
            self.fields["section"].initial = self.instance.category.section.pk
