"""Rides URLs."""

# Django
from django.urls import include, path

# Third party integration
from rest_framework import routers

# Views
from api.purchases.views import PurchaseLineView

router = routers.DefaultRouter()
router.register(
    r"purchase/line",
    PurchaseLineView,
    basename="purchase_line",
)
urlpatterns = [
    path("", include(router.urls)),
]
