"""File to define multiple payments"""

# Django
from django.db import models
from django.db.models import Sum
from django_fsm import FSMIntegerField

# Models
from tracing.models import BaseModel
from ..transitions import PaymentTransitions


class Payment(BaseModel, PaymentTransitions):
    """Payment model"""

    workflow = PaymentTransitions.workflow
    wizard = models.ForeignKey(
        to="profiles.Profile", verbose_name="mago", on_delete=models.CASCADE
    )
    state = FSMIntegerField(
        choices=workflow.choices,
        default=workflow.CREATED,
        protected=True,
        verbose_name="estado",
    )
    url = models.URLField(verbose_name="url", editable=False, blank=True, null=True)

    def __str__(self):
        date = f"{self.created_date.day}/{self.created_date.month}/{self.created_date.year}"
        return f"{str(self.wizard)}. {date}"

    def total_payments(self):
        payments = self.lines.aggregate(total=Sum("amount"))
        return payments.get("total")

    class Meta:
        verbose_name = "Pago"
        verbose_name_plural = "Pagos"


class PaymentLine(BaseModel):
    """Payment line model"""

    payment = models.ForeignKey(
        to=Payment, verbose_name="Pago", on_delete=models.CASCADE, related_name="lines"
    )
    amount = models.FloatField(verbose_name="cantidad")
    verbose = models.CharField(verbose_name="leyenda", max_length=128)
    link = models.URLField(verbose_name="url", blank=True, null=True)
    short_link = models.URLField(
        verbose_name="short url", blank=True, null=True, editable=False
    )
