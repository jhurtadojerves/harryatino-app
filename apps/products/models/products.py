"""Product model"""

# Python
from io import BytesIO

# Django
from django.db import models
from django.db.models.signals import post_save
from django.core import files

# Models
from tracing.models import BaseModel
from apps.products.models import Category
from ..utils import get_upload_path

# Third party integrations
import requests


class Product(BaseModel):
    """Product model."""

    name = models.CharField(max_length=128, unique=True, verbose_name="Nombre")
    reference = models.CharField(
        max_length=10, verbose_name="Referencia", unique=True
    )  # I am sorry 2^n, but this value is very important
    points = models.PositiveIntegerField(verbose_name="Puntos")
    cost = models.PositiveIntegerField(verbose_name="Precio")
    initial_stock = models.PositiveIntegerField(verbose_name="Stock inicial", default=1)
    image = models.URLField(verbose_name="Imagen")
    uploaded_image = models.ImageField(
        verbose_name="Imagen", null=True, upload_to=get_upload_path, blank=True
    )
    description = models.TextField(verbose_name="Descripción")
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        verbose_name="Categoría",
        related_name="products",
    )
    slug = models.SlugField(max_length=256, editable=False)
    can_be_sold = models.BooleanField(default=False, verbose_name="¿Puede ser vendido?")

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

    def get_image(self):
        if self.uploaded_image:
            return self.uploaded_image.url
        return self.image

    def __str__(self):
        return f"{self.name} - {self.reference}"

    class Meta(BaseModel.Meta):
        verbose_name = "Producto"
        verbose_name_plural = "Productos"
        ordering = ("pk",)


def download_from_imgur_and_upload(sender, instance, created, **kwargs):
    if not instance.uploaded_image and instance.image:
        response = requests.get(instance.image, stream=True)
        if response.status_code == requests.codes.ok:
            file_name = instance.image.split("/")[-1]
            fp = BytesIO()
            fp.write(response.content)
            instance.uploaded_image.save(file_name, files.File(fp))


post_save.connect(download_from_imgur_and_upload, sender=Product)
