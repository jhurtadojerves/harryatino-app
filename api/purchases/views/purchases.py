# DRF
from django.forms.models import model_to_dict
from rest_framework import status
from rest_framework.mixins import CreateModelMixin, DestroyModelMixin, ListModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

# Local
from api.purchases.serializers.purchases import PurchaseLineSerializer
from apps.ecommerce.models import Purchase, PurchaseLine
from apps.products.models import Product


class PurchaseLineView(
    CreateModelMixin, ListModelMixin, DestroyModelMixin, GenericViewSet
):
    serializer_class = PurchaseLineSerializer

    def get_queryset(self):
        return PurchaseLine.objects.filter(
            purchase__user=self.request.user,
        )

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        data = serializer.data

        product = data.get("product")
        product = Product.objects.get(pk=product)

        purchase = data.get("purchase")
        purchase = Purchase.objects.get(pk=purchase)
        lines = purchase.lines.count()

        data_product = model_to_dict(product, fields=["pk", "name", "reference"])
        data_product.update({"available_stock": product.available_stock})
        data.update({"product": data_product, "lines": str(lines)})
        return Response(
            data,
            status=status.HTTP_201_CREATED,
            headers=headers,
        )

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        product = instance.product
        purchase = instance.purchase
        self.perform_destroy(instance)

        lines = purchase.lines.count()

        data_product = {"available_stock": product.available_stock}
        data_product.update(
            **model_to_dict(product, fields=["pk", "name", "reference"])
        )
        data = {"product": data_product, "lines": str(lines)}

        return Response(data=data, status=status.HTTP_202_ACCEPTED)
