# Third party integration
from superadmin.decorators import register

# Base
from config.base import BaseSite
from config.mixins import NotPermissionRequiredMixin


@register("pages.Page")
class PageSite(BaseSite):
    list_mixins = (NotPermissionRequiredMixin,)
    detail_mixins = (NotPermissionRequiredMixin,)
    prepopulate_slug = ("name",)
