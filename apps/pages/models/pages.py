"""Model to Sales"""
# Django
from django.db import models
from django.urls import reverse
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as for_humans
from django.utils.text import slugify
from django.db.models.signals import post_save


# Models
from tracing.models import BaseModel


# Third Party Integration Models
from ckeditor.fields import RichTextField

# Slug


class Page(BaseModel):
    """Sale model."""

    name = models.CharField(max_length=128, unique=True)
    content = RichTextField()
    show_in_home_page = models.BooleanField(default=False)
    slug = models.SlugField(max_length=256, editable=False)

    def __str__(self):
        return self.name

    def clean(self):
        if (
            self.pk
            and Page.objects.filter(show_in_home_page=True).exclude(pk=self.pk).exists()
            and self.show_in_home_page
        ):
            raise ValidationError(
                for_humans(
                    f"Ya existe una página registrada para mostrarse en la página de inicio"
                )
            )
        if (
            (not self.pk)
            and Page.objects.filter(show_in_home_page=True).exists()
            and self.show_in_home_page
        ):
            raise ValidationError(
                for_humans(
                    f"Ya existe una página registrada para mostrarse en la página de inicio..."
                )
            )

    class Meta(BaseModel.Meta):
        """Class Meta"""

        verbose_name = "Página"
        verbose_name_plural = "Páginas"
        ordering = ("id",)
