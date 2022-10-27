# Third party integration
from superadmin.decorators import register

# Base
from config.base import BaseSite
from config.mixins import NotPermissionRequiredMixin

# Forms
from .forms import ProductForm, StockFormset, StockRequestForm

# Local
from .mixins import (
    ProductDetailMixin,
    ProductEditMixin,
    ProductListMixin,
    StockRequestDetail,
    StockRequestFormMixin,
)


@register("products.Product")
class ProductSite(BaseSite):
    list_mixins = (NotPermissionRequiredMixin, ProductListMixin)
    detail_mixins = (NotPermissionRequiredMixin, ProductDetailMixin)
    form_mixins = (ProductEditMixin,)
    form_class = ProductForm
    prepopulate_slug = ("reference",)
    list_template_name = None
    detail_template_name = None
    menu_is_public = True
    paginate_by = 20


@register("products.Section")
class SectionSite(BaseSite):
    list_mixins = (NotPermissionRequiredMixin,)
    detail_mixins = (NotPermissionRequiredMixin,)
    prepopulate_slug = ("name",)
    detail_fields = ("name", "order")


@register("products.Category")
class CategorySite(BaseSite):
    list_mixins = (NotPermissionRequiredMixin,)
    detail_mixins = (NotPermissionRequiredMixin,)
    detail_fields = "name", "section", "available_by_default"


@register("products.StockRequest")
class StockRequestSite(BaseSite):
    detail_mixins = (StockRequestDetail,)
    form_mixins = (StockRequestFormMixin,)
    form_class = StockRequestForm
    inlines = {"lines": StockFormset}

    list_fields = ("name", "status_request")

    detail_template_name = None
    form_template_name = None
