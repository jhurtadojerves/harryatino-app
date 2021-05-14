"""Product model"""

# Django
from django.db import models
from django.db.models.signals import post_save
from django.utils.translation import gettext_lazy as for_humans


# Models
from apps.products.models import Section
from tracing.models import BaseModel


class Category(BaseModel):
    """Category model."""

    name = models.CharField(max_length=32, verbose_name="Nombre", unique=True)
    section = models.ForeignKey(
        Section,
        on_delete=models.PROTECT,
        related_name="categories",
        verbose_name="Sección",
    )
    available_by_default = models.BooleanField(
        default=True, verbose_name="Disponible al crear"
    )

    def __str__(self):
        return f"{str(self.section)} {self.name}"

    def show_name(self):
        if self.name == "LH":
            return "Libros de Hechizos"
        return self.name

    class Meta(BaseModel.Meta):
        """Class Meta."""

        verbose_name = "Categoría"
        verbose_name_plural = "Categorías"
