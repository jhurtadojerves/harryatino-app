from django.conf import settings

from apps.products.models import Product
from apps.sales.models import Sale
from apps.utils.services import TopicAPIService
from apps.workflows.exceptions import WorkflowException


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
                        vip_sale=sale.vip_sale,
                        is_award=sale.is_award,
                        product=sale.product,
                    )
                )

            new_stock = sale.product.stock - sale.quantity

            if sale.vip_sale or sale.is_award:
                new_stock += sale.quantity

            if new_stock < 0:
                raise WorkflowException(
                    f"El producto {sale.product.name} no tiene stock"
                )

            sale.product.stock = new_stock
            products.append(sale.product)

        sales = Sale.objects.bulk_create(sales)
        Product.objects.bulk_update(products, fields=["stock"])
        multiple.sales.add(*sales)

        cls.create_post(multiple)

    @classmethod
    def create_post(cls, multiple):
        sales = multiple.ordered_sales()
        profile = multiple.profile
        response, html = TopicAPIService.create_post(
            topic=profile.get_boxroom_number,
            context={
                "profile": profile,
                "date": multiple.date,
                "sales": sales,
                "legend": multiple.legend,
                "base_url": settings.SITE_URL.geturl(),
                "points": {
                    "creatures": multiple.get_creatures_points_sales,
                    "objects": multiple.get_objects_points_sales,
                },
            },
            template="sales/posts/user_vault.html",
            author=multiple.profile.forum_user_id,
        )
        multiple.url = response.get("url")
        multiple.html = html
        multiple.save(update_fields=["url", "html"])
