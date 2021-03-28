"""Categories model"""

# Django
from django.db import models
from django.db.models.signals import post_save

# Utils

# Models
from tracing.models import BaseModel


class Section(BaseModel):
    """Section mode."""

    name = models.CharField(max_length=128, verbose_name="Nombre", unique=True)
    order = models.IntegerField()
    slug = models.SlugField(max_length=256, editable=False)

    def __str__(self):
        return self.name

    def number_of_products(self):
        number = 0
        categories = self.categories.all()
        if self.name == "Pociones":
            categories = Section.objects.get(name="Objetos").categories.all()
        for category in categories:
            products = category.products
            if self.name == "Pociones":
                products = category.products.filter(reference__icontains="P")
            if self.name == "Objetos":
                products = category.products.exclude(reference__icontains="P")

            number = number + products.count()
        return number

    class Meta(BaseModel.Meta):
        """Class Meta."""

        verbose_name = "Sección"
        verbose_name_plural = "Secciones"
        ordering = ("order",)
