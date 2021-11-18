"""Model to Sales"""
# Django
from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as for_humans
from django.urls import reverse

# Models
from tracing.models import BaseModel
from apps.products.models import Product
from apps.profiles.models import Profile


class Sale(BaseModel):
    """Sale model."""

    date = models.DateField(verbose_name="Fecha")
    product = models.ForeignKey(
        Product, on_delete=models.PROTECT, verbose_name="Producto", related_name="sales"
    )
    profile = models.ForeignKey(
        Profile,
        on_delete=models.PROTECT,
        verbose_name="Comprador",
        related_name="sales",
    )
    available = models.BooleanField(
        default=True,
        verbose_name="Disponible?",
        help_text="Este campo se utiliza para marcar una compra de libros de hechizos o consumibles"
        "Spell books. True = Can Use"
        "Consumables. True = Consumable Used"
        "Creatures. True = In the creature pool",
    )
    vip_sale = models.BooleanField(verbose_name="Compra con llaves HL", default=False)
    is_award = models.BooleanField(
        verbose_name="Premio de Gala (sin importar stock)", default=False
    )
    buyer = models.ForeignKey(
        "authentication.User", verbose_name="vendedor", on_delete=models.PROTECT
    )

    # This field is used to mark a purchase of spell books or consumables.
    # Spell books. True = Can Use
    # Consumables. True = Consumable Used
    # Creatures True = In the creature pool

    def __str__(self):
        return f"{self.date} - {str(self.product)}"

    def clean(self):
        if not self.pk:
            if self.product.check_stock() == 0:
                if self.vip_sale or self.is_award:
                    self.product.initial_stock = self.product.initial_stock + 1
                    self.product.save()
                else:
                    raise ValidationError(
                        for_humans(
                            f"No se puede vender {self.product.name} ya que su stock actual es 0"
                        )
                    )
        elif self.pk:
            sale = Sale.objects.get(pk=self.pk)
            if sale.product.pk != self.product.pk and self.product.check_stock() == 0:
                raise ValidationError(
                    for_humans(
                        f"No se puede vender {self.product.name} ya que su stock actual es 0"
                    )
                )

    class Meta(BaseModel.Meta):
        """Class Meta"""

        verbose_name = "Venta"
        verbose_name_plural = "Ventas"
        ordering = ("date",)
