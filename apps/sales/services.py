from apps.products.models import Product
from apps.sales.models import Sale


class SaleService:
    @classmethod
    def create_sales_from_multiple_sale(cls, multiple):

        sales = []
        products = []

        for sale in multiple.multiple_sales.all():
            for number in range(0, sale.quantity):
                sales.append(
                    Sale(
                        date=multiple.date,
                        profile=multiple.profile,
                        available=sale.available,
                        buyer=multiple.buyer,
                        vip_sale=multiple.vip_sale,
                        is_award=multiple.is_award,
                        product=sale.product,
                    )
                )
            new_stock = max(0, sale.product.stock - sale.quantity)
            sale.product.stock = new_stock
            products.append(sale.product)

        sales = Sale.objects.bulk_create(sales)
        Product.objects.bulk_update(products, fields=["stock"])
        multiple.sales.add(*sales)
