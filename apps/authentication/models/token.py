"""User model."""

from uuid import uuid4

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.template.loader import render_to_string
from django.urls import reverse
from django_fsm import FSMIntegerField

from apps.authentication.transitions import UserTokenTransitions


class AccessToken(models.Model, UserTokenTransitions):
    """Create a random token for login"""

    workflow = UserTokenTransitions.workflow

    created_date = models.DateTimeField(
        auto_now_add=True, verbose_name="fecha de creación"
    )
    modified_date = models.DateTimeField(
        auto_now=True, verbose_name="última fecha de modificación"
    )

    token = models.UUIDField(
        unique=True,
        default=uuid4,
        editable=False,
    )
    state = FSMIntegerField(
        choices=workflow.choices,
        default=workflow.SEND,
        protected=True,
        verbose_name="estado",
    )

    user = models.OneToOneField(
        "authentication.User", on_delete=models.CASCADE, related_name="token"
    )

    class Meta(AbstractUser.Meta):
        """Class Meta."""

        verbose_name = "Token de acceso"
        verbose_name_plural = "Tokens de acceso"

    def __str__(self):
        return f"Código de Acceso de {self.user.__str__()}"

    @property
    def profile(self):
        return self.user.profile

    @property
    def get_login_url(self):
        base_url = settings.SITE_URL.geturl()
        token_url = reverse("auth:login_witch_token", args=[str(self.token)])
        return f"{base_url}{token_url}"

    def send_message(self):
        from apps.utils.services import UserAPIService

        title = "Cuenta en el Magic Mall creada correctamente"
        body = render_to_string(
            "authentication/send_personal_message.html",
            context={
                "nick": self.profile.nick,
                "token": self.get_login_url,
                "topic_id": settings.TOPIC_QUESTIONS,
            },
        )

        UserAPIService.send_personal_message(
            to_users_id=[str(self.profile.forum_user_id)], title=title, body=body
        )
        UserAPIService.download_user_data_and_update(self.profile)
