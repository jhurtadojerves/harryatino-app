# Django
from django.db import models

# Base
from tracing.models import BaseModel

# Local
from apps.dynamicforms.choices import TypesOfFieldChoices


class Field(BaseModel):
    """Class define model Fields"""

    type = models.CharField(
        max_length=64, choices=TypesOfFieldChoices.choices, verbose_name="Tipo de campo"
    )
    label = models.CharField(max_length=256)
    name = models.CharField(max_length=256, null=True)
    widget = models.TextField(blank=True, null=True)
    required = models.BooleanField(default=True, verbose_name="Es requerido?")
    form = models.ForeignKey(
        "dynamicforms.Form",
        on_delete=models.PROTECT,
        related_name="field_form",
        verbose_name="Formulario",
    )
    fieldset = models.ForeignKey(
        "dynamicforms.Fieldset",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        verbose_name="Categoria",
    )

    class Meta:
        """Class information"""

        verbose_name = "Campo"
        verbose_name_plural = "Campos"
        ordering = ["form", "fieldset", "pk"]
        unique_together = ("form", "label")

    def __str__(self):
        """Overwrite method return str"""
        return "%s [%s]" % (self.label, self.type)


class Fieldset(BaseModel):
    """Class define model Fieldsets"""

    name = models.CharField(max_length=128, verbose_name="Nombre")

    class Meta:
        """Class information"""

        verbose_name = "Sección del formulario"
        verbose_name_plural = "Secciones del formulario"
        ordering = ["name"]

    def __str__(self):
        """Overwrite method return str"""
        return "%s" % self.name


class Form(BaseModel):
    """Class define model the forms"""

    name = models.CharField(max_length=128, verbose_name="Nombre")
    description = models.TextField(null=True, blank=True, verbose_name="Descripción")

    class Meta:
        """Class information"""

        verbose_name = "Formulario"
        verbose_name_plural = "Formularios"
        ordering = ["name"]

    def __str__(self):
        """Overwrite method return str"""
        return "%s" % self.name

    @property
    def get_fieldsets(self):
        fieldsets = {}
        fields = self.field_form.all().values("fieldset", "name")

        for field in fields:
            key = field.get("fieldset", None)
            value = field.get("name", "")
            if key in fieldsets:
                lista = list(fieldsets.get(key))
                if isinstance(lista, list):
                    lista.append(value)
                fieldsets.update({key: tuple(lista)})
            else:
                fieldsets.update({key: tuple([value])})
        return tuple(fieldsets.values())
