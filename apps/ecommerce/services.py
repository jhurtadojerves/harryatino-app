from datetime import datetime

from apps.products.models import Product
from apps.sales.models import Sale


class PurchaseService:
    @classmethod
    def create_sales(cls, purchase, buyer):
        date = datetime.now()
        profile = purchase.user.profile
        sales = []
        products = []

        for sale in purchase.lines.select_related("product"):
            sales.append(
                Sale(
                    date=date,
                    profile=profile,
                    available=sale.product.category.available_by_default,
                    buyer=buyer,
                    product=sale.product,
                )
            )
            new_stock = max(0, sale.product.stock - 1)
            new_reserved_stock = max(0, sale.product.reserved_stock - 1)
            sale.product.stock = new_stock
            sale.product.reserved_stock = new_reserved_stock
            products.append(sale.product)

        created_sales = Sale.objects.bulk_create(sales)
        Product.objects.bulk_update(products, fields=["stock", "reserved_stock"])

        purchase.sales.add(*created_sales)

    @classmethod
    def reject_purchase(cls, purchase):
        products = []

        for line in purchase.lines.select_related("product"):
            line.product.reserved_stock -= 1
            products.append(line.product)

        Product.objects.bulk_update(products, fields=["reserved_stock"])

    @classmethod
    def update_stock(cls):
        pass
