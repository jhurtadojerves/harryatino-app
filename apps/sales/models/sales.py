"""Model to Sales"""
# Django
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Q, Sum
from django.utils.translation import gettext_lazy as for_humans

# Third party integration
from django_fsm import FSMIntegerField

# Models
from tracing.models import BaseModel

from apps.profiles.models import Profile
from apps.sales.transitions import MultipleSateTransitions, SaleTransitions


class Sale(BaseModel, SaleTransitions):
    """Sale model."""

    workflow = SaleTransitions.workflow
    date = models.DateField(verbose_name="Fecha")
    state = FSMIntegerField(
        choices=workflow.choices,
        default=workflow.CREATED,
        protected=True,
        verbose_name="estado",
    )
    product = models.ForeignKey(
        "products.Product",
        on_delete=models.PROTECT,
        verbose_name="Producto",
        related_name="sales",
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
        help_text="Este campo se utiliza para marcar una compra de libros de hechizos "
        "o consumibles. <br>"
        "Libros de Hechizos. Marcado = Se puede usar<br>"
        "Consumibles. Desmarcado = Consumible utilizado<br>"
        "Criaturas (Premios y/o Régimen Transitorio). "
        "Desmarcado = La criatura se encuentra en la reserva de animales<br>",
    )
    vip_sale = models.BooleanField(verbose_name="Compra con llaves HL", default=False)
    is_award = models.BooleanField(
        verbose_name="Premio de Gala (sin importar stock)", default=False
    )
    buyer = models.ForeignKey(
        "authentication.User", verbose_name="vendedor", on_delete=models.PROTECT
    )
    consumable_comment = models.TextField(
        verbose_name="Comentario", blank=True, null=True
    )
    consumable_url = models.URLField(verbose_name="URL uso", null=True)
    payment = models.ForeignKey(
        to="payments.Payment",
        on_delete=models.SET_NULL,
        verbose_name="Pago",
        null=True,
        editable=False,
    )

    # This field is used to mark a purchase of spell books or consumables.
    # Spell books. True = Can Use
    # Consumables. True = Consumable Used
    # Creatures True = In the creature pool

    def __str__(self):
        return f"{self.date} - {str(self.product)}"

    def clean(self):
        if not self.pk:
            if self.product.stock <= 0:
                if not (self.vip_sale or self.is_award):
                    raise ValidationError(
                        for_humans(
                            f"No se puede vender {self.product.name} "
                            f"ya que su stock actual es 0"
                        )
                    )
            else:
                self.product.stock = max(self.product.stock - 1, 0)
                self.product.save()
        elif self.pk:
            # TODO: Define logic for change stock
            sale = Sale.objects.get(pk=self.pk)

            if sale.product.pk != self.product.pk and self.product.stock == 0:
                raise ValidationError(
                    for_humans(
                        f"No se puede vender {self.product.name} "
                        f"ya que su stock actual es 0"
                    )
                )
            elif sale.product.pk != self.product.pk:
                sale.product.stock = sale.product.stock + 1
                self.product.stock = self.product.stock - 1
                self.product.save()
                sale.product.save()

    @property
    def get_sale_level(self):
        if self.product.level_book():
            return f"Nivel {self.product.level_book()}"
        else:
            return f"{self.product.category.name}"

    class Meta(BaseModel.Meta):
        """Class Meta"""

        verbose_name = "Venta"
        verbose_name_plural = "Ventas"
        ordering = ("id",)
        permissions = [
            ("can_send_to_payment", "Puede enviar la compra para pago"),
        ]


class MultipleSale(BaseModel, MultipleSateTransitions):
    workflow = MultipleSateTransitions.workflow

    date = models.DateField(verbose_name="Fecha")
    vip_sale = models.BooleanField(verbose_name="Compra con llaves HL", default=False)
    is_award = models.BooleanField(
        verbose_name="Premio de Gala (sin importar stock)", default=False
    )
    state = FSMIntegerField(
        choices=workflow.choices,
        default=workflow.DRAFT,
        protected=True,
        verbose_name="estado",
    )

    # Relations
    buyer = models.ForeignKey(
        "authentication.User", verbose_name="vendedor", on_delete=models.PROTECT
    )
    products = models.ManyToManyField(
        "products.Product", through="SaleMultipleSale", verbose_name="productos"
    )
    profile = models.ForeignKey(
        Profile,
        on_delete=models.PROTECT,
        verbose_name="Comprador",
    )
    sales = models.ManyToManyField(to=Sale, verbose_name="ventas")

    def ordered_sales(self):
        return self.sales.order_by(
            "product__category__section__order",
            "product__category__name",
            "product__name",
        )

    def __str__(self):
        return f"Compras de {self.profile.__str__()} #{self.id}"

    @property
    def get_creatures_points_sales(self):
        product__points = (
            self.sales.filter(product__category__name__startswith="X")
            .distinct()
            .aggregate(sum=Sum("product__points"))
            .get("sum", 0)
        )
        return product__points if product__points else 0

    @property
    def get_objects_points_sales(self):
        product__points = (
            self.sales.filter(
                Q(product__category__name__startswith="A")
                | Q(product__category__name__startswith="P")
            )
            .distinct()
            .aggregate(sum=Sum("product__points"))
            .get("sum", 0)
        )
        return product__points if product__points else 0


class SaleMultipleSale(models.Model):
    product = models.ForeignKey(
        "products.Product", on_delete=models.CASCADE, verbose_name="Producto"
    )
    sale = models.ForeignKey(
        MultipleSale,
        on_delete=models.CASCADE,
        verbose_name="Venta",
        related_name="multiple_sales",
    )
    available = models.BooleanField(
        default=True,
        verbose_name="Disponible?",
        help_text="Este campo se utiliza para marcar una compra de libros de hechizos "
        "o consumibles. <br>"
        "Libros de Hechizos. Marcado = Se puede usar<br>"
        "Consumibles. Desmarcado = Consumible utilizado<br>"
        "Criaturas (Premios y/o Régimen Transitorio). "
        "Desmarcado = La criatura se encuentra en la reserva de animales<br>",
    )
    quantity = models.PositiveIntegerField(verbose_name="Cantidad", default=1)

    class Meta:
        unique_together = ("product", "sale")
