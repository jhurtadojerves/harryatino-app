"""Choices payments models"""
from django.db import models


class PropertiesChoices(models.IntegerChoices):
    FAMILY = 0, "Familia"
    BUSINESS = 1, "Negocio"
