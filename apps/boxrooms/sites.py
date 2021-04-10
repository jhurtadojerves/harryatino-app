# Third party integration
from superadmin.decorators import register

# Base
from config.base import BaseSite
from config.mixins import NotPermissionRequiredMixin
from .forms import BoxroomForm


@register("boxrooms.Boxroom")
class BoxroomSite(BaseSite):
    list_mixins = (NotPermissionRequiredMixin,)
    detail_mixins = (NotPermissionRequiredMixin,)
    form_class = BoxroomForm
    form_template_name = None
    menu_is_public = True

    detail_template_name = None
