"""Announcements sites"""

# Hydra
from config.base import BaseSite
from superadmin.decorators import register


# Models
from .models import Announcement

# Mixins
from .mixins import AnnouncementListMixin, AnnouncementDetailMixin
from config.mixins import NotPermissionRequiredMixin


@register("announcements.Announcement")
class AnnouncementSite(BaseSite):
    """Site for Announcements"""

    list_mixins = (
        NotPermissionRequiredMixin,
        AnnouncementListMixin,
    )
    detail_mixins = (NotPermissionRequiredMixin, AnnouncementDetailMixin)

    form_template_name = None
    list_template_name = None
    detail_template_name = None
    menu_is_public = True
