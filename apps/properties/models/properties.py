"""Base model to properties"""
# Django
# Third Party Integration Models
from ckeditor.fields import RichTextField
from django.db import models

# Models
from tracing.models import BaseModel

# Choices
from ..choices import PropertiesChoices


class Property(BaseModel):
    name = models.CharField(max_length=128, unique=True, verbose_name="Nombre")
    content = RichTextField(verbose_name="Contenido", null=True, blank=True)
    owner = models.ManyToManyField(
        "profiles.Profile", verbose_name="Propietarios/Patriarcas"
    )
    vault = models.IntegerField(unique=True, verbose_name="Número de bóveda")
    inscription = models.IntegerField(
        unique=True, verbose_name="Número de topic de inscripción"
    )
    rol = models.IntegerField(unique=True, verbose_name="Número de topic de rol")
    property_type = models.IntegerField(
        choices=PropertiesChoices.choices, verbose_name="Tipo de propiedad"
    )

    def __str__(self):
        return f"{self.get_property_type_display()} {self.name}"

    class Meta:
        verbose_name = "propiedad"
        verbose_name_plural = "propiedades"
