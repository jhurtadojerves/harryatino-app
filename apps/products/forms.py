# Django
from django.forms import ModelForm, inlineformset_factory, forms

from apps.products.models import StockRequest, StockProduct
from django_select2.forms import ModelSelect2Widget

# Models
from apps.products.models import Product, Category


class ProductUpdateForm(ModelForm):
    class Meta:
        model = Product
        fields = (
            "name",
            "reference",
            "points",
            "cost",
            "image",
            "description",
            "category",
        )
        widgets = {
            "category": ModelSelect2Widget(
                model=Category,
                search_fields=["name__icontains", "section__name__icontains"],
                max_results=10,
                attrs={
                    "class": "form-control form-control-sm",
                    "data-placeholder": "Buscar Categoría",
                    "data-minimum-input-length": 0,
                },
            )
        }


class ProductCreateForm(ProductUpdateForm):
    class Meta(ProductUpdateForm.Meta):
        fields = ProductUpdateForm.Meta.fields + ("initial_stock",)


class StockRequestForm(ModelForm):
    """Form for book"""

    class Meta:
        model = StockRequest
        fields = ("name", "forum_url")


StockFormset = inlineformset_factory(
    StockRequest,
    StockProduct,
    fields=("product", "requested_amount"),
    extra=0,
    min_num=1,
    validate_min=1,
    widgets={
        "product": ModelSelect2Widget(
            model=Product,
            search_fields=["name__icontains",],
            max_results=10,
            attrs={
                "class": "form-control form-control-sm",
                "data-placeholder": "Buscar Producto",
                "data-minimum-input-length": 2,
            },
        )
    },
)
