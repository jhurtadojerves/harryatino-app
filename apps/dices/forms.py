# Third party integration
from django import forms
from django_select2 import forms as s2forms
from django_select2.forms import ModelSelect2MultipleWidget, ModelSelect2Widget
from superadmin.forms import ModelForm

from apps.dices.models import Dice, Roll, Topic


class BaseRollDiceForm:
    MODIFIER_CHOICES = [
        ["none", "Ninguno"],
        ["+", "Sumar"],
        ["-", "Restar"],
        ["*", "Multiplicar"],
        ["/", "Dividir"],
    ]

    sides = forms.IntegerField(
        label="Número de caras",
        min_value=2,
        help_text="Cantidad de caras que tendrá cada dado."
        "<br /> Es un número positivo",
        initial=6,
    )
    number = forms.IntegerField(
        label="Cantidad de dados",
        min_value=1,
        help_text="Número de dados que se lanzará. "
        "Todos los dados tendrán la misma cantidad de caras",
        initial=1,
    )
    modifier = forms.ChoiceField(
        label="Modificador",
        choices=MODIFIER_CHOICES,
        widget=forms.RadioSelect,
        help_text="Operación que se realizará con el resultado de cada dado",
        required=False,
    )
    modifier_value = forms.IntegerField(
        label="Valor a modificar",
        min_value=1,
        help_text="Valor modificador para cada resultado "
        "(Suma, resta, multiplicación, división)",
        initial=1,
    )
    result_operation = forms.BooleanField(
        label="¿Sumar resultados?",
        help_text="Indica si se sumaran los resultados de cada dado "
        "o se presentarán individualmente",
        required=False,
    )

    fieldsets = (
        (
            "number",
            "sides",
        ),
        (
            "modifier",
            "modifier_value",
        ),
        "result_operation",
    )


class TopicForm(ModelForm):
    class Meta:
        model = Topic
        fieldsets = (
            (
                "topic_id",
                "category",
            ),
            "permissions",
            "allow_custom",
        )
        widgets = {
            "category": ModelSelect2Widget(
                model="dices.Category",
                search_fields=[
                    "name__unaccent__icontains",
                ],
                max_results=20,
                attrs={
                    "data-minimum-input-length": 0,
                },
            ),
            "permissions": ModelSelect2MultipleWidget(
                model="authentication.User",
                search_fields=[
                    "profile__nick__unaccent__icontains",
                ],
                max_results=20,
                attrs={
                    "data-minimum-input-length": 0,
                },
            ),
        }


class RollForm(ModelForm):
    sides = BaseRollDiceForm.sides  # noqa
    number = BaseRollDiceForm.number  # noqa
    modifier = BaseRollDiceForm.modifier  # noqa
    modifier_value = BaseRollDiceForm.modifier_value  # noqa
    result_operation = BaseRollDiceForm.result_operation  # noqa

    class Meta:
        model = Roll
        fieldsets = BaseRollDiceForm.fieldsets


class DiceForm(ModelForm):
    sides = BaseRollDiceForm.sides  # noqa
    number = BaseRollDiceForm.number  # noqa
    modifier = BaseRollDiceForm.modifier  # noqa
    modifier_value = BaseRollDiceForm.modifier_value  # noqa
    result_operation = BaseRollDiceForm.result_operation  # noqa

    class Meta:
        model = Dice
        fieldsets = (
            (
                "name",
                "categories",
            ),
            (
                "number",
                "sides",
            ),
            (
                "modifier",
                "modifier_value",
            ),
            "result_operation",
        )
        widgets = {
            "categories": ModelSelect2MultipleWidget(
                model="dices.Category",
                search_fields=[
                    "name__unaccent__icontains",
                ],
                max_results=20,
                attrs={
                    "data-minimum-input-length": 0,
                },
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        initial = kwargs.get("initial", {})
        configuration = initial.get("configuration", {})

        if self.instance and self.instance.pk:
            configuration = self.instance.configuration

        if configuration:
            self.fields["sides"].initial = configuration.get("sides", 6)
            self.fields["number"].initial = configuration.get("number", 1)
            self.fields["modifier"].initial = configuration.get("modifier", "none")
            self.fields["modifier_value"].initial = configuration.get(
                "modifier_value", 1
            )
            self.fields["result_operation"].initial = configuration.get(
                "result_operation", False
            )


class CustomDiceForm(ModelForm):
    dice = forms.ModelChoiceField(
        queryset=Dice.objects.filter(is_active=True).order_by("name"),
        widget=s2forms.ModelSelect2Widget(
            model=Dice,
            search_fields=[
                "name",
            ],
            max_results=100,
            attrs={
                "data-minimum-input-length": 0,
            },
        ),
        label="Dado",
    )

    class Meta:
        model = Roll
        fields = ["dice"]
