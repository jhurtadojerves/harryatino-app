from django.http import Http404

from apps.ecommerce.workflows import PurchaseWorkflowChoices
from config.mixins.filteriing import FilterByChoice
from config.model_site import CustomFieldServiceMixin


class PurchaseListMixin(FilterByChoice):
    CHOICES = PurchaseWorkflowChoices.choices
    SEARCH_PARAM = "state"


class PurchaseDetailMixin(CustomFieldServiceMixin):
    def get_object(self):
        obj = super().get_object()
        user = self.request.user

        if not user.is_moderator and obj.user != user:
            raise Http404(f"No se encontró la compra con id {obj.pk}")

        return obj
