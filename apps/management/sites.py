from superadmin.decorators import register

from apps.management.mixins import LevelUpdateMixin, ProfileHistoryDetailMixin
from config.base import BaseSite


@register("management.LevelUpdate")
class LevelUpdateSite(BaseSite):
    form_mixins = [LevelUpdateMixin]
    allow_views = (
        "list",
        "create",
        "detail",
    )
    detail_template_name = None
    list_fields = ("id", "created_date", "state")


@register("management.ProfileHistory")
class ProfileHistorySite(BaseSite):
    detail_mixins = [ProfileHistoryDetailMixin]
    allow_views = (
        "list",
        "detail",
    )
    list_fields = ("id", "created_date", "forum_user_id", "profile", "created_user")
    detail_fields = [["forum_user_id:id del foro", "profile: Perfil de comprador"]]
    list_template_name = None
    detail_template_name = None
