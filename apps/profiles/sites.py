"""Profiles sites"""

from superadmin.decorators import register

from config.base import BaseSite
from config.mixins.permissions import NotPermissionRequiredMixin

from .forms import WizardForm
from .mixins import ProfileDetailMixin, ProfileFormMixin, ProfileListMixin


@register("profiles.Profile")
class ProfileSite(BaseSite):
    """Site for Profiles"""

    list_mixins = (NotPermissionRequiredMixin, ProfileListMixin)
    detail_mixins = (NotPermissionRequiredMixin, ProfileDetailMixin)
    form_mixins = (ProfileFormMixin,)
    list_fields = (
        "pk:numero_de_comprador",
        "forum_user_id",
        "nick",
        "magic_level",
        "range_of_creatures",
        "range_of_objects",
    )
    detail_fields = [
        ["pk:numero_de_comprador", "forum_user_id", "nick"],
        ["magic_level", "galleons"],
    ]
    search_fields = ("nick",)
    list_template_name = None
    detail_template_name = None
    menu_is_public = True
    form_class = WizardForm
    allow_views = ("create", "list", "detail")
