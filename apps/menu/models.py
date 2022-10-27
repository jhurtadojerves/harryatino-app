"""Add field to define public menu"""

# Models
# Django
from django.db import models

# Superadmin
from superadmin.models import Menu as BaseMenu
from tracing.models import BaseModel


class Menu(BaseModel):
    public = models.ForeignKey(
        BaseMenu,
        verbose_name="Menú público",
        on_delete=models.CASCADE,
        related_name="public_menus",
    )
