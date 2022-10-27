"""Define models to User Profile"""

from django.db import models
from tracing.models import BaseModel

from config.utils import get_encoded_verbose


class Profile(BaseModel):
    forum_user_id = models.PositiveIntegerField(unique=True, verbose_name="Id del foro")
    nick = models.CharField(max_length=128)
    magic_level = models.PositiveIntegerField(verbose_name="Nivel Mágico")
    galleons = models.IntegerField(verbose_name="Galeones", default=0)
    range_of_creatures = models.CharField(
        max_length=32, verbose_name="Rango de Criaturas"
    )
    range_of_objects = models.CharField(max_length=32, verbose_name="Rango de Objetos")
    vault_number = models.IntegerField(verbose_name="Número de Bóveda")
    boxroom_number = models.IntegerField(
        verbose_name="Número de Bóveda Trastero", null=True, blank=True
    )
    character_sheet = models.IntegerField(
        verbose_name="Número de Ficha de Personaje", null=True, blank=False
    )
    avatar = models.URLField(null=True, blank=True)
    accumulated_posts = models.IntegerField(
        verbose_name="posteos acumulados", editable=False, default=0
    )
    salary_scale = models.TextField(
        verbose_name="escalafón laboral", editable=False, default="T0", max_length=2
    )
    user = models.OneToOneField(
        "authentication.User",
        verbose_name="Usuario",
        null=True,
        blank=True,
        related_name="profile",
        on_delete=models.SET_NULL,
    )

    def __str__(self):
        return self.nick

    def clean_nick(self):
        return get_encoded_verbose(self.nick)

    def calculate_salary_scale(self):
        posts = self.accumulated_posts
        if 1 <= posts <= 100:
            return "T1"
        elif 101 <= posts <= 200:
            return "T2"
        elif 201 <= posts <= 400:
            return "T3"
        elif 401 <= posts <= 700:
            return "T4"
        elif 701 <= posts <= 1000:
            return "T6"
        elif 1001 <= posts <= 2000:
            return "T7"
        elif posts >= 2000:
            return "T7"
        else:
            return "T0"

    def calculate_payment_value(self):
        salary_scale = self.salary_scale
        switcher = {
            "T0": 0,
            "T1": 5000,
            "T2": 6000,
            "T3": 7000,
            "T4": 8000,
            "T5": 9000,
            "T6": 10000,
            "T7": 15000,
        }
        return switcher.get(salary_scale, 0)

    @property
    def get_boxroom_number(self):
        if self.boxroom_number and self.boxroom_number != 75080:
            return self.boxroom_number

        return self.character_sheet

    @property
    def number_of_consumables(self):
        return self.sales.filter(
            product__category__name__startswith="CS", available=True
        ).count()

    @property
    def books(self):
        return self.sales.filter(product__category__name__startswith="LH")

    class Meta(BaseModel.Meta):
        """Meta options."""

        verbose_name = "Mago"
        verbose_name_plural = "Magos"
        ordering = ("pk",)
