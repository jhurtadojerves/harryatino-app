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
    BUY = 0, "Compra"
    OTHER = 99, "Otro"
