# Third party integration
from superadmin.decorators import register

from apps.dices.forms import DiceForm, RoadsDiceFormset, TopicForm
from apps.dices.mixins import (
    DiceMixin,
    TopicDetailMixin,
    TopicFormMixin,
    TopicListMixin,
)

# Base
from config.base import BaseSite
from config.mixins import NotPermissionRequiredMixin


@register("dices.Topic")
class TopicSite(BaseSite):
    list_mixins = (NotPermissionRequiredMixin, TopicListMixin)
    detail_mixins = (NotPermissionRequiredMixin, TopicDetailMixin)
    form_mixins = (TopicFormMixin,)
    form_class = TopicForm
    detail_template_name = None
    menu_is_public = True
    list_fields = ("topic_id", "__str__", "category", "state", "created_date")


@register("dices.Category")
class CategorySite(BaseSite):
    pass


@register("dices.Dice")
class DiceSite(BaseSite):
    form_class = DiceForm
    form_mixins = [DiceMixin]
    detail_fields = ("name", "configuration")
    detail_template_name = None
    inlines = (RoadsDiceFormset,)


@register("dices.Road")
class RoadSite(BaseSite):
    pass
