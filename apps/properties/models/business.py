"""Model to Sales"""
# Django
from django.db import models


# Base
from .base import Property


class Business(Property):
    """Sale model."""

    class Meta:
        """Class Meta"""

        verbose_name = "Negocio"
        verbose_name_plural = "Negocios"
        ordering = ("id",)
