# Third party integration
from superadmin.decorators import register

# Base
from config.mixins import NotPermissionRequiredMixin
from config.model_site import DefaultSite
from .forms import PageForm


@register("pages.Page")
class PageSite(DefaultSite):
    form_class = PageForm
    list_mixins = (NotPermissionRequiredMixin,)
    detail_mixins = (NotPermissionRequiredMixin,)
    form_template_name = None
    detail_template_name = None
    prepopulate_slug = ("name",)
    menu_is_public = True
    url_detail_suffix = None
