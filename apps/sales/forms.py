"""Forms file"""

# Django
from django.forms import Form
from django import forms

# Local
from apps.sales.models import Sale
from apps.products.models import Product
from apps.profiles.models import Profile

# Third Party Integration
from django_select2.forms import ModelSelect2Widget
from superadmin.forms import ModelForm


class SaleForm(ModelForm):
    """Sale form"""

    class Meta:
        model = Sale
        # fields = ("date", "product", "profile", ("available", "vip_sale"))
        # fields = ("date", "product", "profile", "available", "vip_sale")
        fieldsets = {
            "Información de la Venta": ("date", "product", "profile"),
            "Información Adicional": ("available", "vip_sale", "is_award"),
        }
        widgets = {
            "product": ModelSelect2Widget(
                model=Product,
                search_fields=["name__icontains"],
                max_results=10,
                queryset=Product.objects.exclude(name__iendswith="VA"),
                attrs={
                    "class": "form-control form-control-sm",
                    "data-placeholder": "Buscar Producto",
                    "data-minimum-input-length": 0,
                },
            ),
            "profile": ModelSelect2Widget(
                model=Profile,
                search_fields=["forum_user_id__istartswith", "nick__icontains"],
                max_results=10,
                attrs={
                    "class": "form-control form-control-sm",
                    "data-placeholder": "Buscar Comprador",
                    "data-minimum-input-length": 0,
                },
            ),
        }
