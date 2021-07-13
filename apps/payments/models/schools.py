"""Model to schools payments"""
# Django
from django.db import models

# Third party integration
from tracing.models import BaseModel

# Choices
from ..choices import SchoolPaymentLineChoices


class School(BaseModel):
    """Create school models"""

    name = models.CharField(max_length=128, verbose_name="nombre", unique=True)
    slug = models.SlugField(editable=False)

    def __str__(self):
        return self.name

    class Meta(BaseModel.Meta):
        verbose_name = "Escuela Mágica"


class SchoolPayment(BaseModel):
    name = models.CharField(max_length=128, verbose_name="name")
    date = models.DateField(verbose_name="fecha")

    def __str__(self):
        return self.name

    class Meta(BaseModel.Meta):
        verbose_name = "Pago Escuela"


class SchoolPaymentLine(BaseModel):
    payment = models.ForeignKey(
        "payments.SchoolPayment",
        verbose_name="pago a realizar",
        related_name="lines",
        on_delete=models.PROTECT,
    )
    wizard = models.ForeignKey(
        "profiles.Profile",
        verbose_name="mago",
        related_name="school_payments",
        on_delete=models.CASCADE,
    )
    payment_type = models.SmallIntegerField(
        choices=SchoolPaymentLineChoices.choices, verbose_name="Tipo de pago"
    )
    quantity = models.PositiveIntegerField(verbose_name="cantidad")

    def __str__(self):
        return f"{self.payment} de {self.wizard}"
