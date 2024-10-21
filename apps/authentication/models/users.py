"""User model."""

# Django
from django.contrib.auth.models import AbstractUser
from django.db import models


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
    forum_user_id = models.IntegerField(
        verbose_name="ID del foro", null=True, blank=True
    )
    is_moderator = models.BooleanField(default=False, verbose_name="Es moderador")
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = []

    def __str__(self):
        """Return username."""

        if hasattr(self, "profile"):
            return self.profile.nick

        return self.username

    def purchase(self):
        return self.purchases.filter(state__in=[1, 2]).last()

    def products_in_checkout(self):
        return self.purchases.filter(state__in=[1, 2]).last().lines.count()

    @property
    def get_profile(self):
        return self.profile

    class Meta(AbstractUser.Meta):
        """Class Meta."""

        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"
