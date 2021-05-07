"""Product model"""

# Django
from django.db import models

# Models
from tracing.models import BaseModel
from apps.products.models import Category


class Product(BaseModel):
    """Product model."""

    name = models.CharField(max_length=128, unique=True, verbose_name="Nombre")
    reference = models.CharField(
        max_length=10, verbose_name="Referencia", unique=True
    )  # I am sorry 2^n, but this value is very important
    points = models.PositiveIntegerField(verbose_name="Puntos")
    cost = models.PositiveIntegerField(verbose_name="Precio")
    initial_stock = models.PositiveIntegerField(verbose_name="Stock inicial")
    image = models.URLField(verbose_name="Imagen")
    description = models.TextField(verbose_name="Descripción")
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        verbose_name="Categoría",
        related_name="products",
    )
    slug = models.SlugField(max_length=256, editable=False)

    def check_stock(self):
        return self.initial_stock - self.sales.all().count()

    def fix_stock(self):
        stock = self.check_stock()
        if stock < 0:
            stock = stock * -1
            self.initial_stock += stock
            self.save()

    def number_of_sales(self):
        return self.sales.count()

    def level_book(self):
        if self.category.name == "LH":
            return int(self.reference[3:6])
        else:
            return False

    def number(self):
        return self.id

    def __str__(self):
        return f"{self.name} - {self.reference}"

    class Meta(BaseModel.Meta):
        verbose_name = "Producto"
        verbose_name_plural = "Productos"
        ordering = ("pk",)
