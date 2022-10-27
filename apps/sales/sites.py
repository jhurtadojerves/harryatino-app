"""Sales sites"""
# Third party integration
from superadmin.decorators import register

# Forms
from apps.sales.forms import SaleForm
from config.base import BaseSite

# Utils
from config.mixins import NotPermissionRequiredMixin

# Mixins
from .mixins import SaleDetailMixin, SaleFormMixin, SaleListMixin


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
