from django.apps import AppConfig


class ManagementAppConfig(AppConfig):
    name = "apps.management"
    verbose_name = "Administración"
    plural_verbose_name = "Administración"
    menu_sequence = 2
