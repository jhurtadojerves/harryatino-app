"""Mixin for products"""

# Django
from django.contrib import messages
from django.db.models import Q
from django.shortcuts import redirect, reverse
from django.utils.text import slugify
from django.core.paginator import Paginator


# Local
from apps.products.models import Category, Section

# Local
from apps.menu.utils import get_site_url


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
        context.update(
            {
                "search_url": search_url,
                "sections": Section.objects.all(),
                "search_name": search_name,
                "search_value": search_value,
            }
        )
        return context

    def get_queryset(self, *args, **kwargs):
        category = self.request.GET.get("category", False)
        section = self.request.GET.get("section", False)
        name = self.request.GET.get("name", False)
        search_name = dict()
        if name:
            search_name.update({"name__icontains": name})
        queryset = self.model.objects.all()
        if category and Category.objects.filter(name=category.upper()).exists():
            potions = False
            if category in ("P", "PP", "PPP", "PPPP", "PPPPP"):
                category = category.replace("P", "A")
                potions = True
            category = Category.objects.get(name=category.upper())
            if name:
                queryset = self.model.objects.filter(
                    Q(**search_name) | Q(reference__istartswith=name),
                    category=category,
                )
                if potions:
                    queryset = self.model.objects.filter(
                        Q(**search_name) | Q(reference__istartswith=name),
                        category=category,
                        reference__icontains="P",
                    )
                else:
                    queryset = queryset.exclude(reference__icontains="P")
            else:
                queryset = self.model.objects.filter(category=category,)
                if potions:
                    queryset = self.model.objects.filter(
                        category=category, reference__icontains="P"
                    )
                else:
                    queryset = queryset.exclude(reference__icontains="P")

        if section and Section.objects.filter(slug=slugify(section)).exists():
            potions = False
            if section == "Pociones":
                section = "Objetos"
                potions = True
            section = Section.objects.get(slug=slugify(section))
            if name:
                queryset = self.model.objects.filter(
                    Q(**search_name) | Q(reference__istartswith=name),
                    category__section=section,
                )
                if potions:
                    queryset = self.model.objects.filter(
                        Q(**search_name) | Q(reference__istartswith=name),
                        category__section=section,
                        reference__icontains="P",
                    )
                else:
                    queryset = queryset.exclude(reference__icontains="P")
            else:
                queryset = self.model.objects.filter(category__section=section,)
                if potions:
                    queryset = self.model.objects.filter(
                        category__section=section, reference__icontains="P"
                    )
                else:
                    queryset = queryset.exclude(reference__icontains="P")

        if not category and not section and name:
            queryset = self.model.objects.filter(
                Q(**search_name) | Q(reference__istartswith=name)
            )

        return queryset


class ProductDetailMixin:
    slug_field = "reference"

    def get(self, request, *args, **kwargs):
        slug = kwargs.get("slug")
        upper_slug = slug.upper()
        if slug != upper_slug:
            return redirect(
                reverse("site:producto_producto_detalle", args=(upper_slug,)),
                permanent=True,
            )
        return super().get(request, *args, **kwargs)

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


class StockRequestDetail:
    """Stock request Detail View"""

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        status = request.GET.get("status", False)
        if not status:
            return super().get(request, *args, **kwargs)
        if (
            status
            and status == "cancel"
            and request.user.is_superuser
            and self.object.status_request == 1
        ):
            products = self.object.product_requests.all()
            for product in products:
                product.product.initial_stock -= product.requested_amount
                product.product.save()
                self.object.status_request = 2
                self.object.save()
                messages.add_message(
                    request, messages.SUCCESS, "La operación fue cancelada",
                )
                status = False
        if status and not request.user.has_perm("products.can_approve"):
            messages.add_message(
                request, messages.ERROR, "No tienes permisos para realizar esta acción"
            )
        elif not self.object.status_request == 0 and status:
            messages.add_message(
                request,
                messages.ERROR,
                f"No se puede realizara acciones sobre solicitudes con estado {self.object.get_status_request_display()}",
            )
        elif status and status == "approve":
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
        elif status and status == "deny":
            self.object.status_request = 2
            self.object.save()
            messages.add_message(
                request,
                messages.SUCCESS,
                "Solicitud rechazada, no se modificó el stock",
            )
        return redirect(get_site_url(self.object, "detail"))


class StockRequestFormMixin:
    """Stock request form view"""

    def get(self, request, *args, **kwargs):
        self.object = self.get_object_or_none()
        if self.object and not self.object.status_request == 0:
            messages.add_message(
                request,
                messages.ERROR,
                f"No se puede editar solicitudes solicitudes con estado {self.object.get_status_request_display()}",
            )
            return redirect(
                reverse(
                    "site:producto_solicitud-de-stock_detalle", args=[self.object.pk]
                )
            )
        return super().get(request, *args, **kwargs)

    def get_object_or_none(self):
        try:
            return self.get_object()
        except:
            return None
