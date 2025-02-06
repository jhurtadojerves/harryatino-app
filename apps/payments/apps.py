from django.apps import AppConfig


class PaymentConfig(AppConfig):
    name = "apps.payments"
    verbose_name = "Pago"
    plural_verbose_name = "Pagos"
    menu_sequence = 11
