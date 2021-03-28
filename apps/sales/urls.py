# Django
from django.urls import path

# Views
from apps.sales.views import (
    SaleCreate,
    SaleDetail,
    SaleList,
    SaleUpdate,
)

from apps.utils.generate_url import pattern

app_name = "sale"

urlpatterns = [] + pattern(
    prefix="sale",
    url="venta",
    create_view=SaleCreate,
    detail_view=SaleDetail,
    list_view=SaleList,
    update_view=SaleUpdate,
)
