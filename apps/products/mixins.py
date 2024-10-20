"""Mixin for products"""

# Django
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import F, Q
from django.http import Http404
from django.shortcuts import redirect
from django.utils.text import slugify

from apps.menu.utils import get_site_url

# Local
from apps.products.models import Category, Product, Section

from .forms import ProductFormStaff


class ProductListMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        category = self.request.GET.get("category", False)
        section = self.request.GET.get("section", False)
        name = self.request.GET.get("name", False)
        search_url = ""
        search_name = False
        search_value = False
        if name:
            name_value = f"&name={name}"
            search_url = f"&name={name}"
            context.update({"name": name_value, "name_value": name})
        else:
            name_value = ""

        if category:
            search_url = f"&category={category}{name_value}"
            search_name = "category"
            search_value = category
        elif section:
            search_url = f"&section={section}{name_value}"
            search_name = "section"
            search_value = section
        to_stock = self.request.GET.get("to_stock", False)
        from_stock = self.request.GET.get("from_stock", False)
        if to_stock:
            search_url = f"{search_url}&to_stock={to_stock}"
        if from_stock:
            search_url = f"{search_url}&from_stock={from_stock}"
        context.update(
            {
                "to_stock": to_stock if to_stock else "",
                "from_stock": from_stock if from_stock else "",
                "search_url": search_url,
                "sections": Section.objects.all(),
                "search_name": search_name,
                "search_value": search_value,
                "all_records": Product.objects.all(),
            }
        )
        return context

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.annotate(stock_available=F("stock") - F("reserved_stock"))
        exclude_va = self.request.GET.get("exclude_va", True)

        if exclude_va:
            queryset = queryset.exclude(name__endswith="VA")

        category = self.request.GET.get("category", False)
        section = self.request.GET.get("section", False)
        name = self.request.GET.get("search", False)
        search_name = dict()

        if name:
            search_name.update({"name__unaccent__icontains": name})

        if category and Category.objects.filter(name=category.upper()).exists():
            category = Category.objects.get(name=category.upper())

            if name:
                queryset = queryset.filter(
                    Q(**search_name) | Q(reference__istartswith=name),
                    category=category,
                )
            else:
                queryset = queryset.filter(
                    category=category,
                )

        if section and Section.objects.filter(slug=slugify(section)).exists():

            section = Section.objects.get(slug=slugify(section))

            if name:
                queryset = queryset.filter(
                    Q(**search_name) | Q(reference__istartswith=name),
                    category__section=section,
                )
            else:
                queryset = queryset.filter(
                    category__section=section,
                )

        if not category and not section and name:
            queryset = queryset.filter(
                Q(**search_name) | Q(reference__istartswith=name)
            )

        to_stock = self.request.GET.get("to_stock", False)
        from_stock = self.request.GET.get("from_stock", False)

        if not category and not section and not name and (to_stock and from_stock):
            queryset = queryset.filter(
                stock_available__gte=to_stock, stock_available__lte=from_stock
            )

        return queryset.order_by(
            "-can_be_sold",
            "category__id",
            "-stock_available",
            "name",
        )


class ProductDetailMixin:
    slug_field = "reference"

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        slug = kwargs.get("slug")
        upper_slug = slug.upper()
        if slug != upper_slug:
            url = get_site_url(self.object, "detail")
            url = url.replace(slug, upper_slug)
            return redirect(
                url,
                permanent=True,
            )
        return super().get(request, *args, **kwargs)

    def get_object(self):
        queryset = self.get_queryset()
        slug = self.kwargs.get(self.slug_url_kwarg)
        queryset = queryset.filter(reference=slug.upper())
        try:
            obj = queryset.get()
        except queryset.model.DoesNotExist:
            raise Http404(
                f"No {queryset.model._meta.verbose_name} found matching the query"
            )
        return obj

    def get_context_data(self, **kwargs):
        page = self.request.GET.get("page", 1)
        context = super().get_context_data()
        self.object = self.get_object()
        sales = self.object.sales.all()
        paginator = Paginator(sales, per_page=15)
        if int(page) > paginator.num_pages:
            page = paginator.num_pages
        selected_page = paginator.page(page)
        context.update(
            {
                "current_page": selected_page,
                "all_pages": paginator,
                "is_paginated": True,
            }
        )
        return context


class ProductEditMixin:
    slug_field = "reference"
    staff_form = ProductFormStaff

    def get(self, request, *args, **kwargs):

        if self.action == "update":
            self.object = self.get_object()
            slug = kwargs.get("slug")
            upper_slug = slug.upper()
            if slug != upper_slug:
                url = get_site_url(self.object, "update")
                url = url.replace(slug, upper_slug)
                return redirect(
                    url,
                    permanent=True,
                )
        return super().get(request, *args, **kwargs)

    def get_object(self):
        queryset = self.get_queryset()
        slug = self.kwargs.get(self.slug_url_kwarg)
        queryset = queryset.filter(reference=slug.upper())
        try:
            obj = queryset.get()
        except queryset.model.DoesNotExist:
            raise Http404(
                f"No {queryset.model._meta.verbose_name} found matching the query"
            )
        return obj

    def get_form_class(self):
        """Return the form class to use."""
        if self.request.user.is_moderator:
            return self.staff_form
        return self.form_class

class StockRequestFormMixin:
    """Stock request form view"""

    def get(self, request, *args, **kwargs):
        self.object = self.get_object_or_none()

        if self.object and self.object.state != 1:
            messages.add_message(
                request,
                messages.ERROR,
                f"No se puede editar solicitudes con estado "
                f"{self.object.get_state_display()}",
            )
            return redirect(get_site_url(self.object, "detail"))
        return super().get(request, *args, **kwargs)

    def get_object_or_none(self):
        try:
            return self.get_object()
        except Exception:
            return None
