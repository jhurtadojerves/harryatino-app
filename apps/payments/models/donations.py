from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.functional import cached_property
from django_fsm import FSMIntegerField
from tracing.models import BaseModel

from apps.insoles.exceptions import InsolesException
from apps.menu.utils import get_site_url
from apps.payments.transitions import DonationTransitions
from config.fields import CustomURLField


class Donation(BaseModel, DonationTransitions):
    MAX_LINES = 2
    workflow = DonationTransitions.workflow

    request_html = models.TextField(verbose_name="HTML de la solicitud", null=True)
    vault_html = models.TextField(verbose_name="HTML de la bóveda", null=True)
    request_url = CustomURLField(null=True, verbose_name="Link a solicitud")
    vault_discount_url = CustomURLField(null=True, verbose_name="Link al descuento")
    confirm_date = models.DateTimeField(null=True, verbose_name="Fecha de confirmación")

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
        related_name="donations",
    )

    def __str__(self):
        created_date = self.created_date.strftime("%d/%m/%Y")
        return f"Donación de {self.user.profile} ({created_date})"

    def is_full(self):
        return len(self.lines.all()) >= self.MAX_LINES

    @property
    def total(self):
        data = self.lines.aggregate(total=models.Sum("quantity"))

        return data.get("total", 0)

    @property
    def detail_url(self):
        base_url = settings.SITE_URL.geturl()
        path = get_site_url(self, "detail")
        return f"{base_url}{path}"

    @cached_property
    def cached_lines(self):
        return self.lines.all()

    @cached_property
    def columns_detail(self):
        if not len(self.cached_lines):
            return "12"

        return str(int(12 / len(self.cached_lines)))

    class Meta:
        verbose_name = "Donación"
        verbose_name_plural = "Donaciones"
        permissions = (
            ("can_approve_donation", "Can approve donations"),
            ("can_reject_donation", "Can reject donations"),
        )


class DonationLine(BaseModel):
    MIN_QUANTITY_VALUE = 1
    MAX_QUANTITY_VALUE = 4000
    quantity = models.PositiveBigIntegerField(
        validators=[
            MinValueValidator(MIN_QUANTITY_VALUE),
            MaxValueValidator(MAX_QUANTITY_VALUE),
        ],
        verbose_name="cantidad",
    )
    beneficiary = models.ForeignKey(
        to="profiles.Profile",
        verbose_name="Beneficiario",
        on_delete=models.PROTECT,
        null=False,
        related_name="donation_lines",
    )
    vault_html = models.TextField(verbose_name="HTML de la bóveda", null=True)
    vault_deposit_url = CustomURLField(null=True, verbose_name="Link al depósito")
    reason = models.CharField(
        max_length=128, default="--", verbose_name="motivo", blank=True
    )

    donation = models.ForeignKey(
        to="payments.Donation",
        verbose_name="Donación",
        on_delete=models.PROTECT,
        null=False,
        related_name="lines",
    )

    def validate_delete(self, user):
        if self.donation.state != self.donation.workflow.CREATED.value:
            raise InsolesException(
                f"No se pueden editar donaciones en estado {self.donation.get_state_display()}"
            )

        if user != self.donation.user:
            raise InsolesException("Solo puedes eliminar tus propias donaciones")

    def get_insoles_delete_message(self):
        return f"Se eliminó correctamente la donación para {self.beneficiary.nick}"

    @property
    def url_label(self):
        return f"URL del depósito de {self.beneficiary}"

    @property
    def html_label(self):
        return f"HTML del depósito de {self.beneficiary}"
