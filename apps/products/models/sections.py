"""Categories model"""

# Django
from django.db import models
from django.db.models import Count

# Models
from tracing.models import BaseModel

# Utils


class Section(BaseModel):
    """Section mode."""

    name = models.CharField(max_length=128, verbose_name="Nombre", unique=True)
    order = models.IntegerField()
    slug = models.SlugField(max_length=256, editable=False)

    def __str__(self):
        return self.name

    def number_of_products(self):
        result = self.categories.aggregate(products_count=Count("products"))

        return result.get("products_count", 0)

    class Meta(BaseModel.Meta):
        """Class Meta."""

        verbose_name = "Sección"
        verbose_name_plural = "Secciones"
        ordering = ("order",)
