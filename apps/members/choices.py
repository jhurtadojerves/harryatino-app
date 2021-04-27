"""Define choices from model"""

# Base
from django.db import models


class TypesOfFieldChoices(models.TextChoices):
    """Class define choices the type of field"""

    TEXT = "CharField", "Texto"
    EMAIL = "EmailField", "Correo"
    FILE = "FileField", "Archivo"
    HIDDEN = "CharField:HiddenInput", "Campo Oculto"
    TEXTAREA = "CharField:Textarea", "Cuadro de Texto"
    INTEGER = "IntegerField", "Numero Enteros"
    DECIMAL = "DecimalField", "Numero Decimal"
    DATE = "DateField:DateInput", "Fecha"
    CHOICE = "ChoiceField", "Selector"
    RADIO_SELECT = "ChoiceField:RadioSelect", "RadioMultiple"
    CHECKBOX_SELECT_MULTIPLE = (
        "MultipleChoiceField:CheckboxSelectMultiple",
        "CheckboxMultiple",
    )
    BOOLEAN = "BooleanField", "Estado"
    MODEL_CHOICE = "MyChoiceField:MySelect2Widget", "Select2"
