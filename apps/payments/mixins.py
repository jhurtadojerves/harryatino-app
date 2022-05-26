"""Mixins for work site"""
# Django
from django.db.models import Q
from apps.payments.choices import PaymentType
from django.utils.text import slugify


class WorkListMixin:
    def get_queryset(self):
        search = self.request.GET.get("search", False)
        queryset = super().get_queryset()
        if search:
            queryset = queryset.filter(
                Q(wizard__nick__icontains=search)
                | Q(wizard__forum_user_id__icontains=search)
            )
        return queryset


class PaymentListMixin:

    @staticmethod
    def get_search_choices(selected_choice=None):
        choices = []
        for choice in PaymentType.choices:
            choice_id = choice[0]
            choice_display = choice[1]
            slug = slugify(choice_display.replace("/", " "))
            if selected_choice and selected_choice == slug:
                return choice_id
            choices.append({"id": choice_id, "display": choice_display, "slug": slug})
        return choices

    def get_search_selected_choice(self, selected_choice):
        return self.get_search_choices(selected_choice)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        choice_param = self.request.GET.get("choice_param", None)
        random_labels = ["info", "warning"]
        context.update({
            "search_choices": self.get_search_choices(),
            "choice_param": choice_param,
            "random_labels": random_labels
        })
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        choice_param = self.request.GET.get("choice_param", None)
        if choice_param:
            search_choice = self.get_search_selected_choice(choice_param)
            if type(search_choice) == int:
                queryset = queryset.filter(payment_type=search_choice)
        return queryset

