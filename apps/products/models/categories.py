"""Product model"""

# Django
from django.db import models
from tracing.models import BaseModel


class Category(BaseModel):
    """Category model."""

    name = models.CharField(max_length=32, verbose_name="Nombre")
    section = models.ForeignKey(
        "products.Section",
        on_delete=models.PROTECT,
        related_name="categories",
        verbose_name="Sección",
    )
    available_by_default = models.BooleanField(
        default=True, verbose_name="Disponible al crear"
    )

    def __str__(self):
        return self.full_name

    def show_name(self):
        if self.name == "LH":
            return "Libros de Hechizos"
        return self.name

    @property
    def full_name(self):
        return f"{str(self.section)} {self.name}"

    class Meta(BaseModel.Meta):
        """Class Meta."""

        verbose_name = "Categoría"
        verbose_name_plural = "Categorías"
        unique_together = ("name", "section")
