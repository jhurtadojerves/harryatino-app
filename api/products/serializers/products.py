from rest_framework import serializers

from apps.products.models import Product


class ProductSerializer(serializers.ModelSerializer):
    available_by_default = serializers.BooleanField(
        source="category.available_by_default"
    )

    class Meta:
        model = Product
        fields = (
            "pk",
            "reference",
            "name",
            "points",
            "cost",
            "initial_stock",
            "image",
            "uploaded_image",
            "description",
            "available_by_default",
            "slug",
        )
