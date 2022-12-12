"""Model to works"""

# Python
import calendar
import locale
from datetime import datetime

# Django
from django.db import models
from django.db.models.signals import post_save
from django.utils import timezone

# Third party integration
from django_fsm import FSMIntegerField

# Models
from tracing.models import BaseModel

from config.fields import CustomURLField

from ..signals import create_monthly_payment_lines

# Transitions
from ..transitions import (
    MonthlyLineTransitions,
    MonthlyPaymentTransitions,
    PostTransitions,
)


class Work(BaseModel):
    """Work model."""

    wizard = models.ForeignKey(
        "profiles.Profile",
        verbose_name="Usuario",
        on_delete=models.CASCADE,
        unique=True,
    )
    work = models.CharField(verbose_name="Trabajo", max_length=256)
    work_description = models.TextField(
        verbose_name="Descripción del trabajo", blank=True, null=True
    )

    def __str__(self):
        return f"{self.wizard}: {self.work}"

    class Meta(BaseModel.Meta):
        """Class Meta"""

        verbose_name = "Trabajo"
        verbose_name_plural = "Trabajos"
        ordering = ("wizard__forum_user_id",)


class MonthPayment(BaseModel, MonthlyPaymentTransitions):
    """Model to define monthly payment"""

    workflow = MonthlyPaymentTransitions.workflow

    month = models.DateField(verbose_name="Mes y año", default=timezone.now)
    post_url = CustomURLField(
        verbose_name="Link del pedido de pago", blank=True, null=True
    )

    state = FSMIntegerField(
        choices=workflow.choices,
        default=workflow.CREATED,
        protected=True,
        verbose_name="estado",
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

    class Meta(BaseModel.Meta):
        """Class Meta"""

        verbose_name = "Pago CMI"
        verbose_name_plural = "Pagos CMI"
        ordering = ("-pk",)


class MonthPaymentLine(BaseModel, MonthlyLineTransitions):
    workflow = MonthlyPaymentTransitions.workflow

    work = models.ForeignKey(
        "payments.Work",
        verbose_name="Usuario",
        on_delete=models.CASCADE,
        related_name="lines",
    )
    month = models.ForeignKey(
        "payments.MonthPayment",
        on_delete=models.PROTECT,
        verbose_name="Mes y año",
        related_name="lines",
    )
    number_of_posts = models.IntegerField(verbose_name="Número de Posteos", default=0)
    calculated_value = models.IntegerField(verbose_name="Valor a pagar", default=0)
    paid = models.BooleanField(verbose_name="¿Pagado?", editable=False, default=False)
    paid_url = models.URLField(
        verbose_name="Link del pago", editable=False, null=True, blank=True
    )
    state = FSMIntegerField(
        choices=workflow.choices,
        default=workflow.CREATED,
        protected=True,
        verbose_name="estado",
    )

    class Meta:
        unique_together = ("work", "month")
        ordering = ("state", "work__wizard__nick")


class Post(BaseModel, PostTransitions):
    workflow = PostTransitions.workflow

    content = models.JSONField(default=dict, verbose_name="contenido")
    parse_content = models.JSONField(default=dict, verbose_name="contenido parseado")
    month = models.DateField(verbose_name="Mes y año", default=timezone.now)

    state = FSMIntegerField(
        choices=workflow.choices,
        default=workflow.CREATED,
        protected=True,
        verbose_name="estado",
    )

    def last_day(self):
        month = calendar.monthrange(self.month.year, self.month.month)
        last_day_date = datetime(
            self.month.year, self.month.month, month[1], hour=23, minute=59, second=59
        )
        return last_day_date.strftime("%Y-%m-%dT%H:%M:%SZ")

    def first_day(self):
        first_day_date = datetime(self.month.year, self.month.month, 1)
        return first_day_date.strftime("%Y-%m-%dT%H:%M:%SZ")

    def __str__(self):
        locale.setlocale(locale.LC_TIME, "es_ES.UTF-8")
        return self.month.strftime("%B del %Y")


post_save.connect(create_monthly_payment_lines, sender=MonthPayment)
