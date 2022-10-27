"""Product model"""

# Django
from django.db import models
from django.db.models.signals import post_save

# Models
from tracing.models import BaseModel

from apps.products.models import Category
from apps.products.signals import download_from_imgur_and_upload
from apps.products.utils import get_upload_path
from config.utils import get_encoded_verbose


class Product(BaseModel):
    """Product model."""

    can_be_sold = models.BooleanField(default=False, verbose_name="¿Puede ser vendido?")
    cost = models.PositiveIntegerField(verbose_name="Precio")
    description = models.TextField(verbose_name="Descripción")
    image = models.URLField(verbose_name="Imagen")
    initial_stock = models.PositiveIntegerField(verbose_name="Stock inicial", default=1)
    stock = models.PositiveIntegerField(verbose_name="Stock disponible", default=1)
    reserved_stock = models.PositiveIntegerField(
        verbose_name="Stock reservado", default=0
    )

    name = models.CharField(max_length=128, unique=True, verbose_name="Nombre")
    points = models.PositiveIntegerField(verbose_name="Puntos")
    reference = models.CharField(
        max_length=10, verbose_name="Referencia", unique=True
    )  # I am sorry 2^n, but this value is very important
    slug = models.SlugField(max_length=256, editable=False)
    uploaded_image = models.ImageField(
        verbose_name="Imagen", null=True, upload_to=get_upload_path, blank=True
    )

    # Foreign keys
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        verbose_name="Categoría",
        related_name="products",
    )

    @property
    def available_stock(self):
        return self.stock - self.reserved_stock

    @property
    def number_of_sales(self):
        return self.sales.count()

    def level_book(self):
        if self.category.name == "LH":
            return int(self.reference[3:6])
        else:
            return False

    @property
    def level_required(self):
        category = self.category.name
        if not category.startswith("X") and not category.startswith("LH"):
            return 0

        if category.startswith("X"):
            categories = {"X": 0, "XX": 6, "XXX": 11, "XXXX": 21, "XXXXX": 41}
            return categories.get(category, 0)
        else:
            level_book = self.level_book()
            return level_book if level_book else 0

    def get_image(self):
        if self.uploaded_image:
            return self.uploaded_image.url
        return self.image

    def __str__(self):
        return f"{self.name} - {self.reference}"

    @property
    def get_name(self):
        return get_encoded_verbose(self.name)

    def fix_stock(self):
        sales = self.sales.count()
        stock = max(0, self.initial_stock - sales)
        self.stock = stock
        self.save()

    class Meta(BaseModel.Meta):
        verbose_name = "Producto"
        verbose_name_plural = "Productos"
        ordering = ("-can_be_sold", "category__id", "name")


class ProductRefill(BaseModel):
    product = models.ForeignKey(
        to="products.Product", on_delete=models.PROTECT, null=False
    )
    quantity = models.PositiveIntegerField(verbose_name="cantidad")


post_save.connect(download_from_imgur_and_upload, sender=Product)
