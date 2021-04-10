"""Sales sites"""
# Third party integration
from superadmin.decorators import register
from config.base import BaseSite

# Models
from apps.sales.models import Sale

# Utils
from config.mixins import NotPermissionRequiredMixin

# Mixins
from .mixins import SaleListMixin, SaleDetailMixin

# Forms
from apps.sales.forms import SaleForm


@register("sales.Sale")
class SaleSite(BaseSite):
    form_class = SaleForm
    list_fields = ("pk", "date", "product", "profile")
    list_mixins = (NotPermissionRequiredMixin, SaleListMixin)
    detail_mixins = (SaleDetailMixin,)
    list_template_name = None
    detail_template_name = None
    paginate_by = 50
