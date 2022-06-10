"""File to define multiple payments"""

# Django
from django.db import models
from django.db.models import Sum
from django_fsm import FSMIntegerField

# Third party integration
from tracing.models import BaseModel

# Local
from apps.payments.transitions import PaymentTransitions
from apps.payments.choices import PaymentType
from apps.utils.services import LinkService
from config.fields import CustomURLField


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
    payment_type = models.SmallIntegerField(
        choices=PaymentType.choices,
        default=PaymentType.BUY,
        verbose_name="Tipo de pago",
    )
    url = CustomURLField(verbose_name="url", editable=False, blank=True, null=True)
    html = models.TextField(verbose_name="html generado", editable=False, null=True)
    reason = models.CharField(verbose_name="Motivo", blank=True, null=True, default="", max_length=256)

    def __str__(self):
        date = f"{self.created_date.day}/{self.created_date.month}/{self.created_date.year}"
        return f"{str(self.wizard)}. {date}"

    def total_payments(self):
        payments = self.lines.aggregate(total=Sum("amount"))
        return payments.get("total")

    def get_int_total_payments(self):
        return int(self.total_payments())

    def get_lines(self):
        return self.lines.order_by("pk")

    def get_encoded_reason(self):
        reason = self.get_default_reason
        if self.reason:
            reason = self.reason
        a, b = "áéíóúüñÁÉÍÓÚÜÑ", "aeiouunAEIOUUN"
        trans = str.maketrans(a, b)
        translate = reason.translate(trans)
        return str(translate)

    @property
    def get_default_reason(self):
        if self.payment_type == PaymentType.OTHER:
            return "Otros Ingresos"
        elif self.payment_type == PaymentType.OTHER_MINUS:
            return "Otros Descuentos"
        return ""

    class Meta:
        verbose_name = "Pago"
        verbose_name_plural = "Pagos"
        ordering = ("-pk",)
        permissions = [
            ("create_payment_post", "Crear posteo del pago"),
        ]


class PaymentLine(BaseModel):
    """Payment line model"""

    payment = models.ForeignKey(
        to=Payment, verbose_name="Pago", on_delete=models.CASCADE, related_name="lines"
    )
    amount = models.FloatField(verbose_name="cantidad")
    verbose = models.CharField(verbose_name="leyenda", max_length=128)
    link = models.URLField(verbose_name="url", blank=True, null=True)

    def get_encoded_verbose(self):
        a, b = "áéíóúüñÁÉÍÓÚÜÑ", "aeiouunAEIOUUN"
        trans = str.maketrans(a, b)
        translate = self.verbose.translate(trans)
        return str(translate)

    def get_integer_amount(self):
        return int(self.amount)

    def get_shorturl(self):
        return LinkService.get_resolved_short_url(self.link)

    class Meta:
        ordering = ("pk",)
