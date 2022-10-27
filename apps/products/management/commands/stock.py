# Django
from django.core.management.base import BaseCommand

# Models
from apps.products.models import Product


class Command(BaseCommand):
    help = "Migrate stock to new fields"

    def handle(self, *args, **options):
        products = Product.objects.all()
        products_bulk = []

        print(["Inicial", "Ventas", "Nuevo"])

        for product in products:
            sales = product.sales.count()
            stock = max(0, product.initial_stock - sales)
            product.stock = stock
            products_bulk.append(product)
            print([product.initial_stock, sales, stock])

        Product.objects.bulk_update(products_bulk, fields=["stock"])

        self.stdout.write(self.style.SUCCESS("Successfully stock fixed"))
