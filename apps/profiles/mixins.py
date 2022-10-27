"""Define mixins to profile"""


from django.core.paginator import Paginator
from django.db.models import Q
from django.utils.text import slugify

from apps.products.models import Category, Product, Section


class ProfileListMixin:
    """Profile List Mixin"""

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        nick = self.request.GET.get("nick", False)
        forum_id = self.request.GET.get("forum_id", False)
        buyer = self.request.GET.get("buyer", False)
        page = self.request.GET.get("page", 1)
        search_url = ""
        if nick:
            search_url = f"&nick={nick}"
        if forum_id:
            search_url = f"&forum_id={forum_id}"
        if buyer:
            search_url = f"&buyer={buyer}"

        context.update(
            {
                "nick": nick,
                "forum_id": forum_id,
                "buyer": buyer,
                "page": page,
                "search_url": search_url,
            }
        )
        return context

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)

        nick = self.request.GET.get("nick", False)
        forum_id = self.request.GET.get("forum_id", False)
        buyer = self.request.GET.get("buyer", False)
        search_params = dict()
        if nick:
            search_params.update({"nick__icontains": nick})
        elif forum_id:
            search_params.update({"forum_user_id__startswith": forum_id})
        elif buyer:
            search_params.update({"pk": buyer})
        if search_params:
            queryset = queryset.filter(**search_params)
        return queryset


class ProfileDetailMixin:
    def get_context_data(self, **kwargs):
        self.object = self.get_object()
        context = super().get_context_data()
        page = self.request.GET.get("page", 1)
        category = self.request.GET.get("category", False)
        section = self.request.GET.get("section", False)
        sales = self.object.sales.all()
        search_name = False
        search_value = False
        search_url = ""

        if category and Category.objects.filter(name=category.upper()).exists():
            search_url = f"&category={category}"
            search_name = "category"
            search_value = category
            potions = False
            if category in ("P", "PP", "PPP", "PPPP", "PPPPP"):
                category = category.replace("P", "A")
                potions = True
            category = Category.objects.get(name=category.upper())
            sales = self.object.sales.filter(
                product__category=category,
            )
            if potions:
                sales = sales.exclude(~Q(product__reference__icontains="P"))
            else:
                sales = sales.exclude(product__reference__icontains="P")

        if section and Section.objects.filter(slug=slugify(section)).exists():
            search_url = f"&section={section}"
            search_name = "section"
            search_value = section
            potions = False
            if section == "Pociones":
                section = "Objetos"
                potions = True
            section = Section.objects.get(slug=slugify(section))
            sales = self.object.sales.filter(
                product__category__section=section,
            )
            if potions:
                sales = sales.exclude(~Q(product__reference__icontains="P"))
            else:
                sales = sales.exclude(product__reference__icontains="P")
        pages_url = ""
        paginator = Paginator(sales, per_page=8)
        if int(page) > paginator.num_pages:
            page = paginator.num_pages
        selected_page = paginator.page(page)
        last_sale = False
        if sales.exists():
            last_sale = sales.first()
        context.update(
            {
                "search_url": f"{pages_url}{search_url}",
                "all_pages": paginator,
                "page_form": page,
                "current_page": selected_page,
                "sections": Section.objects.all(),
                "search_name": search_name,
                "search_value": search_value,
                "is_paginated": True,
                "last_sale": last_sale,
                "any_product": Product.objects.first(),
            }
        )
        return context
