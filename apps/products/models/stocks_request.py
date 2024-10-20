"""Stock request model"""

# Django
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver

# Models
from django_fsm import FSMIntegerField
from tracing.models import BaseModel

from apps.products.transitions import StockRequestTransitions
from config.fields import CustomURLField


class StockRequest(BaseModel, StockRequestTransitions):
    """Stock request model."""
    workflow = StockRequestTransitions.workflow
    state = FSMIntegerField(
        choices=workflow.choices,
        default=workflow.CREATED,
        protected=True,
        verbose_name="estado",
    )

    class StatusRequest(models.IntegerChoices):
        CREATED = 0, "Creado"
        APPROVED = 1, "Aprobado"
        REJECTED = 2, "Rechazado"

    name = models.CharField(max_length=256, verbose_name="explicación corta del pedido")
    forum_url = CustomURLField(verbose_name="URL del post del foro")
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
        permissions = (("can_approve", "Can approve requests"),)


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
    current_stock = models.PositiveIntegerField(default=0, verbose_name="Stock actual")


@receiver(pre_save, sender=StockProduct)
def update_current_stock(sender, instance: StockProduct, *args, **kwargs):
    instance.current_stock = instance.product.available_stock
