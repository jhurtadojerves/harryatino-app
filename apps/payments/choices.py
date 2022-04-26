"""Choices for payments model"""
from django.db import models


class TypeVaultChoices(models.IntegerChoices):
    USER = 1, "Usuario"
    FAMILY = 2, "Familia"
    COMMERCE = 3, "Negocio"


class SchoolPaymentLineChoices(models.IntegerChoices):
    PAY = 0, "Pago"
    DISCOUNT = 1, "Descuento"


class PaymentType(models.IntegerChoices):
    BUY = 0, "Compra"  # magic_mall
    PLUS = 1, "Pluses"  # plus_equipo
    SCHOLAR_PLUS = 2, "Pago profesores/arcanos/uzzas"  # scholar_plus
    SCHOLAR_PAYMENT = 3, "Pago estudiantes"  # scholar_payment
    SCHOLAR_CHARGE = 4, "Descuento estudiantes"  # scholar_charge
    OTHER = 99, "Otro"
