"""Announcement model."""

# Django
from django.db import models

# Third Party Integration Models
from ckeditor.fields import RichTextField
from tracing.models import BaseModel


class Announcement(BaseModel):
    """Announcement model."""

    name = models.CharField(verbose_name="Nombre del anuncio", max_length=256)
    content = RichTextField(verbose_name="Contenido")

    def __str__(self):
        return self.name

    class Meta(BaseModel.Meta):
        verbose_name = "Anuncio"
        verbose_name_plural = "Anuncios"
