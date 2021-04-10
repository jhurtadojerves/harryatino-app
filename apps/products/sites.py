# Third party integration
from superadmin.decorators import register

# Base
from config.base import BaseSite
from config.mixins import NotPermissionRequiredMixin

# Local
from .mixins import (
    ProductListMixin,
    ProductDetailMixin,
    ProductEditMixin,
    StockRequestFormMixin,
    StockRequestDetail,
)

# Forms
from .forms import ProductForm, StockRequestForm, StockFormset


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
    detail_fields = "name", "section"


@register("products.StockRequest")
class StockRequestSite(BaseSite):
    list_mixins = (NotPermissionRequiredMixin,)
    detail_mixins = (NotPermissionRequiredMixin, StockRequestDetail)
    form_mixins = (StockRequestFormMixin,)
    form_class = StockRequestForm
    inlines = {"lines": StockFormset}

    list_fields = ("name", "status_request")

    detail_template_name = None
    form_template_name = None
