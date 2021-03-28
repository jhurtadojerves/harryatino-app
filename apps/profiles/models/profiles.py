"""Define models to User Profile"""

# Django
from django.db import models
from django.urls import reverse


# Models
from tracing.models import BaseModel


class Profile(BaseModel):
    forum_user_id = models.PositiveIntegerField(unique=True, verbose_name="Id del foro")
    nick = models.CharField(max_length=128)
    magic_level = models.PositiveIntegerField(verbose_name="Nivel Mágico")
    range_of_creatures = models.CharField(
        max_length=8, verbose_name="Rango de Criaturas"
    )
    range_of_objects = models.CharField(max_length=8, verbose_name="Rango de Objetos")
    vault = models.URLField(verbose_name="Bóveda", null=True, blank=True)
    avatar = models.URLField()

    def __str__(self):
        return self.nick

    def update_url(self):
        return reverse("profile:profile_update", args=(self.id,))

    def detail_url(self):
        return reverse("profile:profile_detail", args=(self.id,))

    class Meta(BaseModel.Meta):
        """Meta options."""

        verbose_name = "Mago"
        verbose_name_plural = "Magos"
        ordering = ("pk",)
