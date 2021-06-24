# Django
from django.urls import path

# Views
from .views import CalculatePaymentView, CreatePaymentView

app_name = "payments"

urlpatterns = [
    path(
        "pagos/pagos-cmi/<int:pk>/calcular/",
        CalculatePaymentView.as_view(),
        name="calculate_cmi",
    ),
    path(
        "pagos/pagos-cmi/<int:pk>/pagar/",
        CreatePaymentView.as_view(),
        name="create_cmi_payment",
    ),
]
