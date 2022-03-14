# Django
from django.urls import path

# Views
from .views import UseConsumableFormView

urlpatterns = [
    path(
        route="sales/sale/<int:pk>/form/",
        view=UseConsumableFormView.as_view(),
        name="sales_sale_consumable_form",
    ),
]
