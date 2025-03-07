"""Mixin for products"""

from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import redirect

from apps.menu.templatetags.get_site_url import get_site_url


class SaleListMixin:
    """Mixin from Sale List Site"""

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        (
            product,
            forum_id,
            buyer,
            from_date,
            to_date,
            page,
            search_params,
        ) = self.get_data(self.request)
        search_url = ""
        if from_date and to_date:
            search_url = f"&from_date={from_date}&to_date={to_date}"
        if product:
            search_url = f"&product={product}"
        if forum_id:
            search_url = f"&forum_id={forum_id}"
        if buyer:
            search_url = f"&buyer={buyer}"
        context.update(
            {
                "product": product,
                "forum_id": forum_id,
                "buyer": buyer,
                "page": page,
                "search_url": search_url,
                "from_date": from_date,
                "to_date": to_date,
            }
        )
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        (
            product,
            forum_id,
            buyer,
            from_date,
            to_date,
            page,
            search_params,
        ) = self.get_data(self.request)
        if search_params:
            queryset = queryset.filter(**search_params)
        if from_date and to_date:
            queryset = queryset.filter(date__gte=from_date, date__lte=to_date)
        return queryset

    @staticmethod
    def get_data(request):
        search_params = {}
        product = request.GET.get("product", False)
        forum_id = request.GET.get("forum_id", False)
        buyer = request.GET.get("buyer", False)
        from_date = request.GET.get("from_date", False)
        to_date = request.GET.get("to_date", False)
        page = request.GET.get("page", 1)
        if product:
            search_params.update({"product__name__unaccent__icontains": product})
        if forum_id:
            search_params.update({"profile__forum_user_id__startswith": forum_id})
        if buyer:
            search_params.update({"profile__pk": buyer})

        return product, forum_id, buyer, from_date, to_date, page, search_params


class SaleDetailMixin:
    context_object_name = "sale"


class SaleFormMixin:
    def form_valid(self, form):
        """If the form is valid, save the associated model."""
        self.object = form.save(commit=False)
        if self.action == "create":
            self.object.buyer = self.request.user
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


class MultipleSaleFormMixin:
    def get(self, request, *args, **kwargs):
        self.object = self.get_object_or_none()

        if self.object and not self.object.state == 1:
            messages.add_message(
                request,
                messages.ERROR,
                f"No se puede editar solicitudes solicitudes con estado "
                f"{self.object.get_state_display()}",
            )
            return redirect(get_site_url(self.object, "detail"))

        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        """If the form is valid, save the associated model."""
        self.object = form.save(commit=False)
        if self.action == "create":
            self.object.buyer = self.request.user

        self.object.save()

        for inline in form.inlines:
            inline.instance = self.object
            inline.save()

        return HttpResponseRedirect(self.get_success_url())

    def get_object_or_none(self):
        try:
            return self.get_object()
        except Exception:
            return None


class MultipleSaleDetailMixin:
    def get_context_data(self, *args, **kwargs):
        self.object = self.get_object()
        render = self.request.GET.get("render", False)
        context = super().get_context_data()
        context.update(
            {
                "render": render,
            }
        )

        return context
