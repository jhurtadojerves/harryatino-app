"""User model."""

# Django
from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """Custom user model."""

    created = models.DateTimeField(
        verbose_name="created at",
        auto_now_add=True,
        help_text="Datetime on which the user was created",
    )
    modified = models.DateTimeField(
        verbose_name="modified at",
        auto_now=True,
        help_text="Datetime on which the user was last modified",
    )
    old_number = models.IntegerField(verbose_name="ID anterior", null=True, blank=True)
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = []

    def __str__(self):
        """Return username."""
        return self.username

    class Meta(AbstractUser.Meta):
        """Class Meta."""

        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"
