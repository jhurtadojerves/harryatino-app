"""Sales sites"""
# Third party integration
from superadmin.decorators import register

# Forms
from apps.sales.forms import MultipleSaleForm, MultipleSaleFormset, SaleForm
from config.base import BaseSite

# Utils
from config.mixins import GenericFiltering, NotPermissionRequiredMixin

# Mixins
from .mixins import (
    MultipleSaleDetailMixin,
    MultipleSaleFormMixin,
    SaleDetailMixin,
    SaleFormMixin,
    SaleListMixin,
)


@register("sales.Sale")
class SaleSite(BaseSite):
    form_class = SaleForm
    list_fields = ("pk:código", "date", "product", "profile", "buyer")
    form_mixins = (SaleFormMixin,)
    list_mixins = (NotPermissionRequiredMixin, SaleListMixin)
    detail_mixins = (SaleDetailMixin, NotPermissionRequiredMixin)
    list_template_name = None
    detail_template_name = None
    form_template_name = None
    paginate_by = 50
    menu_is_public = True


@register("sales.MultipleSale")
class MultipleSaleSite(BaseSite):
    form_class = MultipleSaleForm
    form_mixins = (MultipleSaleFormMixin,)
    detail_mixins = (MultipleSaleDetailMixin,)
    list_mixins = (GenericFiltering,)
    search_param = "profile__nick"
    inlines = {"lines": MultipleSaleFormset}

    detail_fields = [["buyer", "profile"], ["date", "vip_sale", "is_award"]]

    detail_template_name = None
    form_template_name = None
