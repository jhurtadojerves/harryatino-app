"""Announcements sites"""

# Hydra
from superadmin.decorators import register

from config.base import BaseSite
from config.mixins import NotPermissionRequiredMixin

from .mixins import AnnouncementDetailMixin, AnnouncementListMixin


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
