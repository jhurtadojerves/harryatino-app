"""Products form"""

# Django
from django import forms
from django.forms import inlineformset_factory

# Third party integration
from django_select2.forms import ModelSelect2Widget
from superadmin.forms import ModelForm

# Local
from apps.products.models import Product, Section, StockProduct, StockRequest


class ProductForm(ModelForm):
    section = forms.ModelChoiceField(
        label="Sección",
        queryset=Section.objects.all(),
        widget=ModelSelect2Widget(
            model="product.Section",
            search_fields=[
                "name__unaccent__icontains",
            ],
            max_results=100,
            attrs={
                "data-minimum-input-length": 0,
            },
        ),
    )

    class Meta:
        model = Product
        fieldsets = (
            (
                "name",
                "reference",
            ),
            ("points", "cost"),
            ("image", "uploaded_image"),
            (
                "section",
                "category",
            ),
            ("description",),
            "can_be_sold",
        )
        widgets = {
            "category": ModelSelect2Widget(
                model="products.Category",
                search_fields=["name__unaccent__icontains"],
                dependent_fields={"section": "section"},
                attrs={
                    "data-minimum-input-length": 0,
                },
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.id:
            self.fields["section"].initial = self.instance.category.section.pk


class StockRequestForm(ModelForm):
    class Meta:
        model = StockRequest
        fieldsets = (
            "name",
            "forum_url",
        )


class ProductFormStaff(ProductForm):
    class Meta(ProductForm.Meta):
        fieldsets = (
            ("name", "reference", "stock"),
            ("points", "cost"),
            ("image", "uploaded_image"),
            (
                "section",
                "category",
            ),
            ("description",),
            "can_be_sold",
        )


StockFormset = inlineformset_factory(
    StockRequest,
    StockProduct,
    fields=("product", "requested_amount"),
    extra=0,
    min_num=1,
    validate_min=1,
    can_delete=True,
    widgets={
        "product": ModelSelect2Widget(
            model=Product,
            search_fields=[
                "name__unaccent__icontains",
            ],
            max_results=10,
            attrs={
                "class": "form-control form-control-sm",
                "data-placeholder": "Buscar Producto",
                "data-minimum-input-length": 2,
            },
        )
    },
)
