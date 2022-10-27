# Django
from django.urls import path

# Views
from .views import (
    CalculatePaymentPropertyView,
    CalculatePaymentView,
    CreatePaymentPropertyView,
    CreatePaymentView,
)

app_name = "payments"

urlpatterns = [
    path(
        route="pagos/pagos-cmi/<int:pk>/calcular/",
        view=CalculatePaymentView.as_view(),
        name="calculate_cmi",
    ),
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
]
