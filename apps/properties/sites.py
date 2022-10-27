# Third party integration
from superadmin.decorators import register

# Base
from config.base import BaseSite
from config.mixins import GenericFiltering, NotPermissionRequiredMixin

from .forms import PropertyForm


@register("properties.Property")
class FamilySite(BaseSite):
    form_class = PropertyForm
    list_mixins = (NotPermissionRequiredMixin, GenericFiltering)
    detail_mixins = (NotPermissionRequiredMixin,)
    form_template_name = None
    detail_template_name = None
    list_template_name = None

    list_fields = ("property_type", "name", "vault", "inscription", "rol")
    detail_fields = (
        ("name", "property_type"),
        ("vault", "inscription", "rol"),
    )
    menu_is_public = True
    search_param = "name"
