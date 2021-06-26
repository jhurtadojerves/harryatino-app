# Third party integration
from superadmin.decorators import register

# Base
from config.base import BaseSite

# Forms
from .forms import WorkMonthForm


@register("payments.Work")
class WorkSite(BaseSite):
    detail_fields = ("wizard", "work", "work_description")
    form_class = WorkMonthForm


@register("payments.MonthPayment")
class MonthPaymentSite(BaseSite):
    detail_fields = ("month",)
    detail_template_name = None
