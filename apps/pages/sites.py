# Third party integration
from superadmin.decorators import register

# Base
from config.base import BaseSite
from config.mixins import NotPermissionRequiredMixin
from .forms import PageForm


@register("pages.Page")
class PageSite(BaseSite):
    form_class = PageForm
    list_mixins = (NotPermissionRequiredMixin,)
    detail_mixins = (NotPermissionRequiredMixin,)
    form_template_name = None
    detail_template_name = None
    prepopulate_slug = ("name",)
    menu_is_public = True
