"""Auth app."""

#  Django
from django.apps import AppConfig


class AuthenticationAppConfig(AppConfig):
    name = "apps.authentication"
    verbose_name = "Autenticación"
    menu_sequence = 3
