"""Social Rank model."""

from django.db import models
from tracing.models import BaseModel


class SocialRank(BaseModel):
    """Social Rank model."""

    name = models.CharField(max_length=128, unique=True, verbose_name="Nombre")
    initial_points = models.PositiveIntegerField(verbose_name="Puntos de Desde")
    end_points = models.PositiveIntegerField(verbose_name="Puntos de Hasta")
    slug = models.SlugField(max_length=256, editable=False)

    def __str__(self):
        return self.name

    class Meta(BaseModel.Meta):
        """Meta options."""

        verbose_name = "Rango Social"
        verbose_name_plural = "Rangos Sociales"
