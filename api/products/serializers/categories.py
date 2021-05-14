import ast
import re

from rest_framework import serializers

from apps.products.models import Category


class ProductSerializers(serializers.ModelSerializer):
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
