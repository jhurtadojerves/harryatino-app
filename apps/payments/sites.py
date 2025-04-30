from superadmin.decorators import register

from config.base import BaseSite
from config.mixins import GenericFiltering

from .forms import DonationForm, PaymentForm, PaymentLineFormset, WorkMonthForm
from .mixins import (
    DonationDetailMixin,
    DonationFormMixin,
    DonationListMixin,
    PaymentListMixin,
    WorkListMixin,
)


# @register("payments.Work")
class WorkSite(BaseSite):
    detail_fields = ("wizard", "work", "work_description")
    list_fields = ("wizard", "work")
    paginate_by = 30
    form_class = WorkMonthForm
    list_mixins = (WorkListMixin,)


# @register("payments.MonthPayment")
class MonthPaymentSite(BaseSite):
    detail_fields = ("month",)
    detail_template_name = None
    fields = ("month", "post_url")


# @register("payments.Post")
class PostSite(BaseSite):
    detail_fields = ("month",)
    fields = ("month",)
    detail_template_name = None


# @register("payments.PropertyPayment")
class PropertyPaymentSite(BaseSite):
    detail_fields = (("month", "payment_type"),)
    list_fields = ("month", "payment_type")

    detail_template_name = None
    list_template_name = None
    list_mixins = (GenericFiltering,)


@register("payments.Payment")
class PaymentSite(BaseSite):
    form_class = PaymentForm
    list_mixins = (PaymentListMixin,)
    inlines = (PaymentLineFormset,)
    list_fields = ("wizard", "payment_type", "state", "created_date")
    detail_fields = (("wizard", "created_date", "url"), "html")
    detail_template_name = None
    list_template_name = None
    paginate_by = 30


@register("payments.Donation")
class Donationsite(BaseSite):
    form_class = DonationForm
    form_mixins = [DonationFormMixin]
    detail_mixins = [DonationDetailMixin]
    list_mixins = [DonationListMixin]
    detail_template_name = None
    list_template_name = None
    allow_views = ("create", "list", "detail")

    detail_fields = {
        "Detalle de Donación": [
            # ["request_html", "vault_html"],
            ["request_url", "vault_discount_url"],
        ],
    }

    list_fields = ["user", "created_date", "confirm_date", "state"]
