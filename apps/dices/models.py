from django.conf import settings
from django.db import models
from django_fsm import FSMIntegerField
from tracing.models import BaseModel

from apps.dices.transitions import TopicTransitions
from apps.dices.workflows import TopicWorkflow
from apps.menu.utils import get_site_url
from config.fields import CustomURLField
from config.middleware import GlobalRequestMiddleware


class Category(BaseModel):
    name = models.CharField(max_length=128, verbose_name="nombre")
    description = models.TextField(verbose_name="descripción")

    class Meta:
        verbose_name = "categoría"
        verbose_name_plural = "categorías"

    def __str__(self):
        return self.name


class Topic(BaseModel, TopicTransitions):
    workflow = TopicWorkflow()
    data = models.JSONField(default=dict)
    topic_id = models.PositiveIntegerField(unique=True)
    state = FSMIntegerField(
        choices=workflow.choices,
        default=workflow.OPEN,
        protected=True,
        verbose_name="estado",
    )
    allow_custom = models.BooleanField(
        verbose_name="Permitir dados personalizados", default=True
    )

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
    permissions = models.ManyToManyField(
        to="authentication.User",
        verbose_name="Usuarios habilitados",
        null=True,
        blank=True,
        help_text="Si no seleccionas ningún usuarios, todos podrán lanzar dados",
    )

    @property
    def dice_is_available(self):
        if self.state != self.workflow.OPEN.value:
            return False

        request = GlobalRequestMiddleware.get_global_request()

        if not request.user.is_authenticated:
            return False

        permissions = self.permissions.all()

        if permissions and not self.permissions.filter(id=request.user.id):
            return False

        return True

    class Meta:
        verbose_name = "topic"
        verbose_name_plural = "topics para dados"
        permissions = (("can_manage", "Can manage dices"),)

    def __str__(self):
        return self.data.get("title")

    @property
    def detail_url(self):
        base_url = settings.SITE_URL.geturl()
        path = get_site_url(self, "detail")
        return f"{base_url}{path}"


class Dice(BaseModel):
    name = models.CharField(max_length=128, verbose_name="Nombre del dado")
    configuration = models.JSONField(default=dict, verbose_name="Configuración")
    categories = models.ManyToManyField(
        to=Category,
        verbose_name="Categorias",
        help_text="Selecciona una o más categorías para este dado",
    )

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

    @property
    def format_values(self):
        configuration = self.configuration
        modifier = (
            "Ninguno"
            if configuration.get("modifier", "Ninguno") == "none"
            else configuration.get("modifier", "Ninguno")
        )
        return {
            "Caras": self.configuration.get("sides", 0),
            "Cantidad de datos": configuration.get("number", 0),
            "Modificador": modifier,
            "Valor a Modificar": self.configuration.get("modifier_value", 0),
            "¿Sumar los resultados?": configuration.get("result_operation", "No"),
        }

    @property
    def categories_string(self):
        categories = self.categories.all()

        if not categories:
            return ""

        categories_str = [category.name for category in categories]
        print(categories_str)

        return ", ".join(categories_str)


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
