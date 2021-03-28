"""Add field to define public menu"""

# Models
from tracing.models import BaseModel

# Superadmin
from superadmin.models import Menu as BaseMenu

# Django
from django.db import models


class Menu(BaseModel):
    public = models.ForeignKey(
        BaseMenu,
        verbose_name="Menú público",
        on_delete=models.CASCADE,
        related_name="public_menus",
    )
