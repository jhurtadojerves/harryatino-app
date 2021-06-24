"""Model to vaults"""
# Django
from django.db import models

# Models
from tracing.models import BaseModel

# Choices
from ..choices import TypeVaultChoices


class Vault(BaseModel):
    """Vault model."""

    title = models.TextField(verbose_name="Nombre de la Bóveda")
    vault_type = models.IntegerField(
        choices=TypeVaultChoices.choices,
        verbose_name="Tipo de bóveda",
        default=TypeVaultChoices.USER,
    )
    identifier = models.IntegerField(verbose_name="Identificador")

    class Meta(BaseModel.Meta):
        """Class Meta"""

        verbose_name = "Trabajo"
        verbose_name_plural = "Trabajos"
        ordering = ("wizard__forum_user_id",)
        unique_together = ("vault_type", "identifier")
