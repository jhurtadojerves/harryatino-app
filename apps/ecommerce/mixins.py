from django.http import Http404

from apps.ecommerce.workflows import PurchaseWorkflowChoices
from config.mixins.filteriing import FilterByChoice
from config.model_site import CustomFieldServiceMixin


class PurchaseListMixin(FilterByChoice):
    CHOICES = PurchaseWorkflowChoices.choices

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        choice_param = self.request.GET.get("choice_param", None)

        if not user.is_moderator:
            queryset = queryset.filter(user=user)

        if choice_param:
            search_choice = self.get_search_selected_choice(choice_param)
            if type(search_choice) == int:  # noqa: E721
                queryset = queryset.filter(state=search_choice)

        return queryset


class PurchaseDetailMixin(CustomFieldServiceMixin):
    def get_object(self):
        obj = super().get_object()
        user = self.request.user

        if not user.is_moderator and obj.user != user:
            raise Http404(f"No se encontró la compra con id {obj.pk}")

        return obj
