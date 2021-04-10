"""Stock request model"""

# Django
from django.db import models
from django.urls import reverse

# Models
from tracing.models import BaseModel


class StockRequest(BaseModel):
    """Stock request model."""

    class StatusRequest(models.IntegerChoices):
        CREATED = 0, "Creado"
        APPROVED = 1, "Aprobado"
        REJECTED = 2, "Rechazado"

    name = models.CharField(max_length=256, verbose_name="explicación corta del pedido")
    forum_url = models.URLField(verbose_name="URL del post del foro")
    products = models.ManyToManyField(
        "products.Product", through="StockProduct", verbose_name="productos"
    )
    status_request = models.IntegerField(
        choices=StatusRequest.choices, default=0, editable=False
    )

    def __str__(self):
        return self.name

    class Meta(BaseModel.Meta):
        verbose_name = "Solicitud de Stock"
        verbose_name_plural = "Solicitudes de Stock"


class StockProduct(models.Model):
    """Custom model to stock request"""

    stock_request = models.ForeignKey(
        "products.StockRequest",
        on_delete=models.CASCADE,
        verbose_name="Cantidad de Stock",
        related_name="product_requests",
    )
    product = models.ForeignKey(
        "products.Product", on_delete=models.CASCADE, verbose_name="Producto"
    )
    requested_amount = models.PositiveIntegerField(
        blank=False, null=False, verbose_name="Cantidad a Aumentar"
    )
