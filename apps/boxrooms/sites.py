# Third party integration
from superadmin.decorators import register

# Base
from apps.boxrooms.forms import BoxroomForm
from apps.boxrooms.mixins import BoxroomListMixin, BoxroomDetailMixin
from config.base import BaseSite
from config.mixins import NotPermissionRequiredMixin


@register("boxrooms.Boxroom")
class BoxroomSite(BaseSite):
    list_mixins = (NotPermissionRequiredMixin, BoxroomListMixin)
    detail_mixins = (NotPermissionRequiredMixin, BoxroomDetailMixin)
    form_class = BoxroomForm
    form_template_name = None
    menu_is_public = True
    detail_template_name = None
