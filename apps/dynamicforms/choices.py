# Django
from django.db import models


class TypesOfFieldChoices(models.TextChoices):
    """Class define choices the type of field"""

    TEXT = "CharField:TextInput", "Texto"
    EMAIL = "EmailField", "Correo"
    FILE = "FileField", "Archivo"
    HIDDEN = "CharField:HiddenInput", "Campo Oculto"
    TEXTAREA = "CharField:Textarea", "Cuadro de Texto"
    INTEGER = "IntegerField:NumberInput", "Numero Enteros"
    DECIMAL = "CharField:NumberInput", "Numero Decimal"
    DATE = "CharField:DateInput", "Fecha"
    CHOICE = "ChoiceField", "Selector"
    MODEL_CHOICE = "MyChoiceField:MySelect2Widget", "Select2 Model"
    RADIO_SELECT = "ChoiceField:RadioSelect", "RadioMultiple"
    CHECKBOX_SELECT_MULTIPLE = (
        "MultipleChoiceField:CheckboxSelectMultiple",
        "CheckboxMultiple",
    )
    BOOLEAN = "BooleanField", "Estado"
