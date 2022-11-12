from django.conf import settings
from django.db import models
from tracing.models import BaseModel

from apps.menu.utils import get_site_url
from config.fields import CustomURLField


class Category(BaseModel):
    name = models.CharField(max_length=128, verbose_name="nombre")
    description = models.TextField(verbose_name="descripción")

    class Meta:
        verbose_name = "categoría"
        verbose_name_plural = "categorías"

    def __str__(self):
        return self.name


class Topic(BaseModel):
    data = models.JSONField(default=dict)
    topic_id = models.PositiveIntegerField(unique=True)

    # Relations
    user = models.ForeignKey(
        to="authentication.User",
        verbose_name="usuario",
        on_delete=models.PROTECT,
        related_name="topics",
    )

    category = models.ForeignKey(
        to=Category,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="categoría",
        related_name="topics",
    )

    class Meta:
        verbose_name = "topic"
        verbose_name_plural = "topics"

    def __str__(self):
        return self.data.get("title")

    @property
    def detail_url(self):
        base_url = settings.SITE_URL.geturl()
        path = get_site_url(self, "detail")
        return f"{base_url}{path}"


class Dice(BaseModel):
    name = models.CharField(max_length=128)
    configuration = models.JSONField(default=dict, verbose_name="Configuración")

    class Meta:
        verbose_name = "Dado predefinido"
        verbose_name_plural = "Dados predefinidos"

    def __str__(self):
        return self.name

    def get_values(self):
        sides = self.configuration.get("sides", 0)
        number = self.configuration.get("number", 0)
        modifier = self.configuration.get("modifier", False)
        modifier_value = self.configuration.get("modifier_value", 0)
        result_operation = self.configuration.get("result_operation", False)

        modifier = None if modifier == "none" else modifier
        modifier_value = None if modifier_value == "" else int(modifier_value)

        return int(sides), int(number), modifier, result_operation, modifier_value


class Roll(BaseModel):
    result = models.TextField(verbose_name="resultado")
    topic = models.ForeignKey(
        to=Topic, verbose_name="topic", on_delete=models.CASCADE, related_name="rolls"
    )
    post_url = CustomURLField(verbose_name="Posteo en el foro", null=True)

    # Relations
    user = models.ForeignKey(
        to="authentication.User",
        verbose_name="usuario",
        on_delete=models.PROTECT,
        related_name="rolls",
    )

    class Meta:
        ordering = ["created_date"]
