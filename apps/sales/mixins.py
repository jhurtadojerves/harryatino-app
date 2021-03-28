"""Mixin for products"""


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
            search_params.update({"product__name__icontains": product})
        if forum_id:
            search_params.update({"profile__forum_user_id__startswith": forum_id})
        if buyer:
            search_params.update({"profile__pk": buyer})

        return product, forum_id, buyer, from_date, to_date, page, search_params
