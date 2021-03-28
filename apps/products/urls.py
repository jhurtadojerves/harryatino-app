# Django
from django.urls import path

# Views
from apps.products.views import (
    ProductCreate,
    ProductDetail,
    ProductList,
    ProductUpdate,
    StockCreate,
    StockDetail,
    StockList,
    StockUpdate,
)

from apps.utils.generate_url import pattern

app_name = "product"

urlpatterns = [] + pattern(
    prefix="product",
    url="producto",
    create_view=ProductCreate,
    detail_view=ProductDetail,
    list_view=ProductList,
    update_view=ProductUpdate,
    slug=True,
)
urlpatterns += pattern(
    prefix="stock",
    url="stock",
    create_view=StockCreate,
    detail_view=StockDetail,
    list_view=StockList,
    update_view=StockUpdate,
)
