"""Models to families payments"""
# Python
import calendar
import locale
from datetime import datetime

# Django
from django.db import models
from django.utils import timezone

# Third party integration
from tracing.models import BaseModel

# Choices
from apps.properties.choices import PropertiesChoices


class PropertyPayment(BaseModel):
    """Monthly payment for properties"""

    month = models.DateField(verbose_name="Mes y año", default=timezone.now)
    payment_type = models.PositiveSmallIntegerField(
        choices=PropertiesChoices.choices, verbose_name="Tipo de pago"
    )

    def __str__(self):
        locale.setlocale(locale.LC_TIME, "es_ES.UTF-8")
        return self.month.strftime("%B del %Y")

    def last_day(self):
        month = calendar.monthrange(self.month.year, self.month.month)
        last_day_date = datetime(
            self.month.year, self.month.month, month[1], hour=23, minute=59, second=59
        )
        return last_day_date.strftime("%Y-%m-%dT%H:%M:%SZ")

    def first_day(self):
        first_day_date = datetime(self.month.year, self.month.month, 1)
        return first_day_date.strftime("%Y-%m-%dT%H:%M:%SZ")

    class Meta:
        verbose_name = "Pago a Familias y Negocios"
        verbose_name_plural = "Pagos a Familias y Negocios"


class PropertyPaymentLine(BaseModel):
    payment = models.ForeignKey(
        PropertyPayment,
        verbose_name="Pago",
        related_name="lines",
        on_delete=models.CASCADE,
    )
    property = models.ForeignKey(
        "properties.Property",
        verbose_name="Propiedad",
        related_name="payments",
        on_delete=models.CASCADE,
    )
    posts = models.PositiveIntegerField(verbose_name="Posteos")
    galleons = models.PositiveIntegerField(verbose_name="Galeones")
    paid = models.BooleanField(default=False)
    paid_url = models.URLField(null=True, editable=False)
