"""Mixin for products"""

# Django
from django.utils.text import slugify
from django.shortcuts import redirect, reverse
from django.db.models import Q

# Local
from apps.products.models import Category, Section


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


class ProductEditMixin:
    slug_field = "reference"
