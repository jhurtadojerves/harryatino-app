# Django
from django.core.management.base import BaseCommand


# Local
from apps.products.models import Product


class Command(BaseCommand):
    help = "Fix product stock if is negative"

    def handle(self, *args, **options):
        products = Product.objects.filter(reference="B0000A0019")
        for product in products:
            product.fix_stock()
        self.stdout.write(self.style.SUCCESS("Successfully stock is fixed"))
