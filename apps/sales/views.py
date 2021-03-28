"""Views for sales"""
from django.contrib.auth.mixins import LoginRequiredMixin

# Views
from apps.utils.views import (
    GenericCreateView,
    GenericDetailView,
    GenericListView,
    GenericUpdateView,
)

from apps.sales.models import Sale
from apps.sales.forms import SaleForm


class SaleCreate(GenericCreateView):
    """Sale Create View"""

    model = Sale
    form_class = SaleForm
    prefix = "sale"
    app_name = "sale"


class SaleUpdate(GenericUpdateView):
    """Sale Create View"""

    model = Sale
    form_class = SaleForm
    prefix = "sale"
    app_name = "sale"


class SaleDetail(LoginRequiredMixin, GenericDetailView):
    """Sale Create View"""

    model = Sale
    template_name = "sales/sales_detail.html"
    fields = "__all__"
    context_object_name = "sale"


class SaleList(LoginRequiredMixin, GenericListView):
    """Sale Create View"""

    model = Sale
    template_name = "sales/sales_list.html"
    context_object_name = "sales"
    paginate_by = 20
    list_display = (
        "id",
        "date",
        "product",
        "profile",
    )
