# Third party integration
from superadmin.decorators import register

# Base
from config.base import BaseSite
from config.mixins import NotPermissionRequiredMixin

# Local
from apps.utils.mixins import LinkDetailMixin


@register("utils.Link")
class LinkSite(BaseSite):
    list_mixins = (NotPermissionRequiredMixin,)
    detail_mixins = (NotPermissionRequiredMixin, LinkDetailMixin)
    allow_views = ("detail",)
