"""Models to purchases"""

from django.conf import settings
from django.db import models
from django.db.models import Q, Sum

# Models
from django.db.models.signals import post_delete, post_save

# Third party integration
from django_fsm import FSMIntegerField
from tracing.models import BaseModel

from apps.ecommerce.signals import cancel_reserve_stock, reserve_stock
from apps.ecommerce.transitions import PurchaseTransitions
from apps.menu.utils import get_site_url
from config.fields import CustomURLField


class Purchase(BaseModel, PurchaseTransitions):
    workflow = PurchaseTransitions.workflow

    state = FSMIntegerField(
        choices=workflow.choices,
        default=workflow.CREATED,
        protected=True,
        verbose_name="estado",
    )

    user = models.ForeignKey(
        to="authentication.User",
        verbose_name="usuario",
        on_delete=models.PROTECT,
        null=False,
        related_name="purchases",
    )
    sales = models.ManyToManyField("sales.Sale", verbose_name="Ventas")
    html = models.TextField(verbose_name="HTML", null=True)
    boxroom_html = models.TextField(verbose_name="HTML trastero", null=True)
    confirm_date = models.DateTimeField(null=True, verbose_name="Fecha de confirmación")
    purchase_url = CustomURLField(
        null=True, verbose_name="Link de la compra en el foro"
    )
    certification_url = CustomURLField(
        null=True, verbose_name="Link de la certificación"
    )
    discount_url = CustomURLField(
        null=True, verbose_name="Link al descuento en la bóveda"
    )

    def __str__(self):
        return (
            f"Compra de {self.user.profile.__str__()} - {self.get_created_date} "
            f"({self.get_state_display()})"
        )

    @property
    def get_creatures_points_sales(self):
        return (
            self.sales.filter(product__category__name__startswith="X")
            .distinct()
            .aggregate(sum=Sum("product__points"))
            .get("sum", 0)
        )

    @property
    def get_objects_points_sales(self):
        return (
            self.sales.filter(
                Q(product__category__name__startswith="A")
                | Q(product__category__name__startswith="P")
            )
            .distinct()
            .aggregate(sum=Sum("product__points"))
            .get("sum", 0)
        )

    @property
    def get_created_date(self):
        return self.created_date.strftime("%d/%m/%Y")

    @property
    def get_number_of_galleons(self):
        return self.lines.aggregate(Sum("product__cost")).get("product__cost__sum")

    @property
    def get_number_of_point(self):
        return self.lines.aggregate(Sum("product__points")).get("product__points__sum")

    @property
    def get_number_of_consumables(self):
        return self.lines.filter(product__category__name__startswith="CS").count()

    @property
    def books(self):
        lines = self.lines.filter(product__category__name__startswith="LH")
        return [line.product for line in lines]

    @property
    def detail_url(self):
        base_url = settings.SITE_URL.geturl()
        path = get_site_url(self, "detail")
        return f"{base_url}{path}"

    class Meta:
        verbose_name = "Compra"
        verbose_name_plural = "Compras"
        permissions = (
            ("can_approve", "Can approve purchases"),
            ("can_reject", "Can reject purchases"),
        )


class PurchaseLine(BaseModel):
    product = models.ForeignKey(
        to="products.Product",
        verbose_name="Producto",
        on_delete=models.SET_NULL,
        null=True,
        related_name="purchase_lines",
    )
    purchase = models.ForeignKey(
        to="ecommerce.Purchase",
        verbose_name="Compra",
        on_delete=models.PROTECT,
        null=False,
        related_name="lines",
    )

    class Meta:
        verbose_name = "línea de compra"
        verbose_name_plural = "líneas de compra"
        unique_together = ["product", "purchase"]


post_save.connect(reserve_stock, sender=PurchaseLine)
post_delete.connect(cancel_reserve_stock, sender=PurchaseLine)
