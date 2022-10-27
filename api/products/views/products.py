"""Define API to Poll model"""

# Django REST Framework
from rest_framework.viewsets import ReadOnlyModelViewSet

from api.products.serializers import ProductSerializer

# Local
from apps.products.models import Product


class ProductViewSet(ReadOnlyModelViewSet):
    """Class to List and Detail the departament"""

    queryset = Product.objects.all()
    serializer_class = ProductSerializer
