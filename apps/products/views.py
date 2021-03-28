"""Views for products"""

# Django
from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.text import slugify
from django.urls import reverse
from django.shortcuts import redirect
from django.db.models import Q

# Mixins
from apps.utils.mixins import FormsetMixin

# Views
from apps.utils.views import (
    GenericCreateView,
    GenericDetailView,
    GenericListView,
    GenericUpdateView,
)

# Models
from apps.products.models import Category, Product, Section, StockRequest

# Forms
from apps.products.forms import (
    StockRequestForm,
    StockFormset,
    ProductUpdateForm,
    ProductCreateForm,
)


class ProductCreate(GenericCreateView):
    """Product Create View"""

    model = Product
    form_class = ProductCreateForm
    prefix = "product"
    app_name = "product"
    template_name = "products/products_form.html"

    def get_success_url(self):
        return reverse("product:product_detail", args=(self.object.slug,))


class ProductUpdate(GenericUpdateView):
    """Product Create View"""

    model = Product
    form_class = ProductUpdateForm
    prefix = "product"
    app_name = "product"
    template_name = "products/products_form.html"

    def get_success_url(self):
        return reverse("product:product_detail", args=(self.object.slug,))


class ProductDetail(GenericDetailView):
    """Product Create View"""

    model = Product
    fields = "__all__"
    template_name = "products/products_detail.html"
    context_object_name = "product"

    def get_context_data(self, **kwargs):
        page = self.request.GET.get("page", 1)
        context = super().get_context_data()
        self.object = self.get_object()
        sales = self.object.sales.all()
        paginator = Paginator(sales, per_page=15)
        if int(page) > paginator.num_pages:
            page = paginator.num_pages
        selected_page = paginator.page(page)
        context.update({"current_page": selected_page, "all_pages": paginator})
        return context


class StockCreate(FormsetMixin, GenericCreateView):
    """Stock Create View"""

    model = StockRequest
    prefix = "stock"
    app_name = "stock"
    template_name = "products/stock_form.html"
    form_class = StockRequestForm
    formset = StockFormset

    def get_success_url(self):
        return reverse("product:stock_detail", args=(self.object.pk,))


class StockUpdate(FormsetMixin, GenericUpdateView):
    """Stock Create View"""

    model = StockRequest
    form_class = StockRequestForm
    formset = StockFormset
    prefix = "stock"
    app_name = "stock"
    template_name = "products/stock_form.html"

    def get_success_url(self):
        return reverse("product:stock_detail", args=(self.object.pk,))

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()

        if not self.object.status_request == 0:
            messages.add_message(
                request,
                messages.ERROR,
                f"No se puede editar solicitudes solicitudes con estado {self.object.get_status_request_display()}",
            )
            return redirect(reverse("product:stock_detail", args=[self.object.pk]))

        return super().get(request, *args, **kwargs)


class StockDetail(LoginRequiredMixin, GenericDetailView):
    """Stock Create View"""

    model = StockRequest
    fields = "__all__"
    context_object_name = "stock"
    template_name = "products/stock_detail.html"

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        status = request.GET.get("status", False)

        if not request.user.is_staff:
            messages.add_message(
                request, messages.ERROR, "No tienes permisos para realizar esta acción"
            )
        elif not self.object.status_request == 0 and status:
            messages.add_message(
                request,
                messages.ERROR,
                f"No se puede realizara acciones sobre solicitudes con estado {self.object.get_status_request_display()}",
            )
        elif status == "approve":
            products = self.object.product_requests.all()
            for product in products:
                product.product.initial_stock += product.requested_amount
                product.product.save()
                self.object.status_request = 1
                self.object.save()
                messages.add_message(
                    request,
                    messages.SUCCESS,
                    "El stock de los productos fue actualizado",
                )
        elif status == "deny":
            self.object.status_request = 2
            self.object.save()
            messages.add_message(
                request,
                messages.SUCCESS,
                "Solicitud rechazada, no se modificó el stock",
            )

        return super().get(request, *args, **kwargs)


class StockList(LoginRequiredMixin, GenericListView):
    """Stock Create View"""

    model = StockRequest
    context_object_name = "stocks"
    paginate_by = 20
    list_display = (
        "name",
        "forum_url",
    )
