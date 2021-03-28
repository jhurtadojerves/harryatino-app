# Third party integration
from superadmin.decorators import register

# Base
from config.base import BaseSite
from config.mixins import NotPermissionRequiredMixin

# Local
from .mixins import ProductListMixin, ProductDetailMixin, ProductEditMixin

# Forms
from .forms import SorterSettingsForm


@register("products.Product")
class ProductSite(BaseSite):
    list_mixins = (NotPermissionRequiredMixin, ProductListMixin)
    detail_mixins = (NotPermissionRequiredMixin, ProductDetailMixin)
    form_mixins = (ProductEditMixin,)
    form_class = SorterSettingsForm
    prepopulate_slug = ("reference",)
    list_template_name = None
    detail_template_name = None


@register("products.Section")
class SectionSite(BaseSite):
    list_mixins = (NotPermissionRequiredMixin,)
    detail_mixins = (NotPermissionRequiredMixin,)
    prepopulate_slug = ("name",)


@register("products.Category")
class CategorySite(BaseSite):
    list_mixins = (NotPermissionRequiredMixin,)
    detail_mixins = (NotPermissionRequiredMixin,)


@register("products.StockRequest")
class StockRequestSite(BaseSite):
    list_mixins = (NotPermissionRequiredMixin,)
    detail_mixins = (NotPermissionRequiredMixin,)
