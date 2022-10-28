"""Transitions for Sales"""

from datetime import datetime

from django.conf import settings
from django_fsm import can_proceed, transition
from tracing.middleware import TracingMiddleware

from apps.ecommerce.conditions import PurchaseConditions
from apps.ecommerce.services import PurchaseService
from apps.ecommerce.workflows import PurchaseWorkflow
from apps.payments.service import PaymentService
from apps.sales.models import Sale
from apps.utils.services import APIService
from apps.workflows.exceptions import WorkflowException


class PurchaseTransitions:
    workflow = PurchaseWorkflow()

    @transition(
        field="state",
        source=[
            workflow.CREATED,
        ],
        target=workflow.CONFIRMED,
        permission="ecommerce.view_purchase",
        conditions=[
            PurchaseConditions.is_owner,
            PurchaseConditions.has_lines,
        ],
        custom=dict(verbose="Confirmar Compra"),
    )
    def confirm(self, **kwargs):
        profile = self.get_updated_profile()
        return
        response, html = APIService.create_post(
            topic=settings.MAGIC_MALL_TOPIC,
            context={"purchase": self, "profile": profile},
            template="ecommerce/posts/user_post.html",
            author=profile.forum_user_id,
        )
        self.html = html
        self.confirm_date = datetime.now()

    @transition(
        field="state",
        source=[
            workflow.CONFIRMED,
        ],
        target=workflow.APPROVED,
        permission="ecommerce.can_approve",
        conditions=[
            PurchaseConditions.is_moderator,
        ],
        custom=dict(verbose="Aprobar Compra"),
    )
    def approve(self, **kwargs):

        profile = self.get_updated_profile()
        information = TracingMiddleware.get_info()
        seller = information.get("user", False)
        PurchaseService.create_sales(self, seller)
        sales_bulk = []
        payment = None

        for sale in self.sales.all():
            payment = PaymentService.get_or_create_payment_for_sale(sale)
            sale.payment = payment
            sales_bulk.append(sale)

        Sale.objects.bulk_update(sales_bulk, fields=["payment"])
        self.sales.all().update(state=Sale.workflow.Choices.PAY)

        if payment and can_proceed(payment.to_pay):
            creatures_points = self.get_creatures_points_sales
            objects_points = self.get_objects_points_sales

            creatures_points = creatures_points if creatures_points else 0
            objects_points = objects_points if objects_points else 0

            payment.to_pay(
                creatures_points=creatures_points, objects_points=objects_points
            )
            payment.save()
            response, html = APIService.create_post(
                topic=profile.get_boxroom_number,
                context={
                    "profile": profile,
                    "sale": self.sales.first(),
                    "sales": self.sales.all(),
                    "base_url": settings.SITE_URL.geturl(),
                    "points": {
                        "creatures": creatures_points,
                        "objects": objects_points,
                    },
                },
                template="ecommerce/posts/user_vault.html",
                author=seller.profile.forum_user_id,
            )
            self.boxroom_html = html
        else:
            raise WorkflowException(str("No se pudo realizar "))

    @transition(
        field="state",
        source=[workflow.CONFIRMED],
        target=workflow.REJECTED,
        permission="ecommerce.can_reject",
        conditions=[
            PurchaseConditions.is_moderator,
        ],
        custom=dict(verbose="Rechazar Compra"),
    )
    def reject(self, **kwargs):
        PurchaseService.reject_purchase(self)

    def get_updated_profile(self):
        profile = APIService.download_user_data_and_update(self.user.profile)

        if profile.galleons < self.get_number_of_galleons:
            raise WorkflowException(
                "No tienes los galeones necesarios para realizar la compra"
            )

        creatures_lines = self.lines.filter(
            product__category__name__startswith="X"
        ).distinct()
        invalide_creatures = [
            line.product
            for line in creatures_lines
            if profile.magic_level < line.product.level_required
        ]

        if invalide_creatures:
            for creature in invalide_creatures:
                raise WorkflowException(
                    f"No tienes el nivel para comprar "
                    f"criaturas {creature.category.name}"
                )

        books_lines = self.lines.filter(
            product__category__name__startswith="LH"
        ).distinct()

        invalide_books_level = [
            line.product
            for line in books_lines
            if profile.magic_level < line.product.level_required
        ]

        if invalide_books_level:
            for book in invalide_books_level:
                raise WorkflowException(
                    f"No tienes el nivel para comprar el {book.name}"
                )

        if self.get_number_of_consumables and profile.number_of_consumables >= 5:
            raise WorkflowException("Has superado el límite de objetos consumibles")

        book_sales = profile.books

        if book_sales and self.books:
            for sale in book_sales:
                if sale.product in self.books:
                    raise WorkflowException(
                        f"No puedes adquirir nuevamente el {sale.product.name}"
                    )

        return profile
