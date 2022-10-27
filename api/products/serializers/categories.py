from rest_framework import serializers

from apps.products.models import Category


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = (
            "pk",
            "name",
            "reference",
            "name",
            "points",
            "cost",
            "initial_stock",
            "image",
            "uploaded_image",
            "description",
            "category",
            "slug",
        )
