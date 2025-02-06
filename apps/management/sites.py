from superadmin.decorators import register

from apps.management.mixins import LevelUpdateMixin
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
