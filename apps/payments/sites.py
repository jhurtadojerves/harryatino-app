# Third party integration
from superadmin.decorators import register

# Base
from config.base import BaseSite

# Forms
from .forms import WorkMonthForm
from .mixins import WorkListMixin


@register("payments.Work")
class WorkSite(BaseSite):
    detail_fields = ("wizard", "work", "work_description")
    list_fields = ("wizard", "work")
    paginate_by = 30
    form_class = WorkMonthForm
    list_mixins = (WorkListMixin,)


@register("payments.MonthPayment")
class MonthPaymentSite(BaseSite):
    detail_fields = ("month",)
    detail_template_name = None
