"""Mixins for work site"""

# Django
from django.db.models import Q

from apps.payments.choices import PaymentType
from config.mixins.filteriing import FilterByChoice


class WorkListMixin:
    def get_queryset(self):
        search = self.request.GET.get("search", False)
        queryset = super().get_queryset()
        if search:
            queryset = queryset.filter(
                Q(wizard__nick__unaccent__icontains=search)
                | Q(wizard__forum_user_id__icontains=search)
            )
        return queryset


class PaymentListMixin(FilterByChoice):
    CHOICES = PaymentType.choices

    def get_queryset(self):
        queryset = super().get_queryset()
        choice_param = self.request.GET.get("choice_param", None)
        if choice_param:
            search_choice = self.get_search_selected_choice(choice_param)
            if type(search_choice) == int:  # noqa: E721
                queryset = queryset.filter(payment_type=search_choice)
        return queryset
