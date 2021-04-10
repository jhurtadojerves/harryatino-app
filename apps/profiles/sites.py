"""Profiles sites"""

# Third party integration
from superadmin.decorators import register
from config.base import BaseSite


# Models
from apps.profiles.models import Profile

# Utils
from config.mixins.permissions import NotPermissionRequiredMixin

# Mixins
from .mixins import ProfileListMixin, ProfileDetailMixin


@register("profiles.Profile")
class ProfileSite(BaseSite):
    """Site for Profiles"""

    list_mixins = (NotPermissionRequiredMixin, ProfileListMixin)
    detail_mixins = (NotPermissionRequiredMixin, ProfileDetailMixin)
    list_fields = (
        "pk:numero_de_comprador",
        "forum_user_id",
        "nick",
        "magic_level",
        "range_of_creatures",
        "range_of_objects",
    )
    search_fields = ("nick",)
    list_template_name = None
    detail_template_name = None
    menu_is_public = True
