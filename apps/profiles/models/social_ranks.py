"""Social Rank model."""

# Django
from django.db import models
from django.db.models.signals import post_save
from django.urls import reverse

# Utils

# Models
from tracing.models import BaseModel


class SocialRank(BaseModel):
    """Social Rank model."""

    name = models.CharField(max_length=128, unique=True, verbose_name="Nombre")
    initial_points = models.PositiveIntegerField(verbose_name="Puntos de Desde")
    end_points = models.PositiveIntegerField(verbose_name="Puntos de Hasta")
    slug = models.SlugField(max_length=256, editable=False)

    def __str__(self):
        return self.name

    def update_url(self):
        return reverse("profile:rank_update", args=(self.slug,))

    def detail_url(self):
        return reverse("profile:rank_detail", args=(self.slug,))

    class Meta(BaseModel.Meta):
        """Meta options."""

        verbose_name = "Rango Social"
        verbose_name_plural = "Rangos Sociales"
