from django.urls import path

from .views import (
    AddBeneficiaryToDonation,
    CalculatePaymentPropertyView,
    CreatePaymentPropertyView,
    CreatePaymentView,
    DonationBeneficiaty,
)

app_name = "payments"

urlpatterns = [
    path(
        route="pagos/pagos-cmi/<int:pk>/pagar/",
        view=CreatePaymentView.as_view(),
        name="create_cmi_payment",
    ),
    # Properties payments
    path(
        route="pago/pagos-a-familias-y-negocios/<int:pk>/calcular/",
        view=CalculatePaymentPropertyView.as_view(),
        name="calculate_properties_payment",
    ),
    path(
        route="pago/pagos-a-familias-y-negocios/<int:pk>/pagar/",
        view=CreatePaymentPropertyView.as_view(),
        name="paid_properties_payment",
    ),
    path(
        route="donations/<int:pk>/form/",
        view=AddBeneficiaryToDonation.as_view(),
        name="donations_form",
    ),
    path(
        route="donations/lines/<int:pk>/edit/",
        view=DonationBeneficiaty.as_view(),
        name="donation_line_edit",
    ),
]
