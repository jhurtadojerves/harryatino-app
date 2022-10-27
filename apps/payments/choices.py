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
    BUY = 0, "Compra"  # magic_mall -
    PLUS = 1, "Pluses"  # plus_equipo +
    SCHOLAR_PLUS = 2, "Pago profesores/arcanos/uzzas"  # scholar_plus
    SCHOLAR_PAYMENT = 3, "Pago estudiantes"  # scholar_payment
    SCHOLAR_CHARGE = 4, "Descuento estudiantes"  # scholar_charge
    CHANGE_OROS = 5, "Cambio de oros por Galeones"
    DUNGEONS = 6, "Recompensa por Mazmorras"
    OTHER = 99, "Otros Depósitos"
    OTHER_MINUS = 100, "Otros Descuentos"

    @classmethod
    def get_plus_choices(cls):
        return (
            cls.PLUS,
            cls.SCHOLAR_PLUS,
            cls.SCHOLAR_PAYMENT,
            cls.CHANGE_OROS,
            cls.DUNGEONS,
            cls.OTHER,
        )

    @classmethod
    def get_minus_choices(cls):
        return cls.BUY, cls.SCHOLAR_CHARGE, cls.OTHER_MINUS
