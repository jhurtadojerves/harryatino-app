"""Rides URLs."""

# Django
from django.urls import include, path

# Third party integration
from rest_framework import routers

# Views
from api.products.views import ProductViewSet

router = routers.DefaultRouter()
router.register(
    r"product", ProductViewSet, basename="product",
)
urlpatterns = [
    path("", include(router.urls)),
]
