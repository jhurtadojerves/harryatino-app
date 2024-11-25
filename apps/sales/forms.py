"""Forms file"""

from django.forms import inlineformset_factory

# Third Party Integration
from django_select2.forms import ModelSelect2Widget
from superadmin.forms import ModelForm

from apps.products.models import Product
from apps.profiles.models import Profile

# Local
from apps.sales.models import MultipleSale, Sale, SaleMultipleSale


class SaleForm(ModelForm):
    """Sale form"""

    class Meta:
        model = Sale
        fieldsets = {
            "Información de la Venta": ("date", "product", "profile"),
            "Información Adicional": ("available", "vip_sale", "is_award"),
        }
        widgets = {
            "product": ModelSelect2Widget(
                model=Product,
                search_fields=["name__unaccent__icontains"],
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
                search_fields=[
                    "forum_user_id__istartswith",
                    "nick__unaccent__icontains",
                ],
                max_results=10,
                attrs={
                    "class": "form-control form-control-sm",
                    "data-placeholder": "Buscar Comprador",
                    "data-minimum-input-length": 0,
                },
            ),
        }


class MultipleSaleForm(ModelForm):
    class Meta:
        model = MultipleSale
        fieldsets = {
            "Información de la Venta": ("date", "profile", "legend"),
        }
        widgets = {
            "profile": ModelSelect2Widget(
                model=Profile,
                search_fields=[
                    "forum_user_id__istartswith",
                    "nick__unaccent__icontains",
                ],
                max_results=10,
                attrs={
                    "class": "form-control form-control-sm",
                    "data-placeholder": "Buscar Comprador",
                    "data-minimum-input-length": 0,
                },
            ),
        }


class SaleConsumableUsedForm(ModelForm):
    class Meta:
        model = Sale
        fields = ("consumable_comment", "consumable_url")


class SaleMultipleSaleForm(ModelForm):
    class Meta:
        model = SaleMultipleSale
        fieldsets = [("product", "quantity"), ("available", "is_award", "vip_sale")]
        widgets = {
            "product": ModelSelect2Widget(
                model=Product,
                search_fields=[
                    "name__unaccent__icontains",
                ],
                max_results=10,
                attrs={
                    "class": "form-control form-control-sm",
                    "data-placeholder": "Buscar Producto",
                    "data-minimum-input-length": 0,
                },
            )
        }


MultipleSaleFormset = inlineformset_factory(
    MultipleSale,
    SaleMultipleSale,
    form=SaleMultipleSaleForm,
    extra=1,
    min_num=1,
    validate_min=1,
    can_delete=True,
)
