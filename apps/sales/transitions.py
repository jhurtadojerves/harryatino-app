"""Transitions for Sales"""


from django_fsm import transition

from apps.sales.workflows import MultipleSaleWorkflow, SaleWorkflow


class SaleTransitions:
    workflow = SaleWorkflow()

    @transition(
        field="state",
        source=[
            workflow.CREATED,
        ],
        target=workflow.PAY,
        permission="sales.can_send_to_payment",
        custom=dict(verbose="Enviar a Pago"),
    )
    def send_to_pay(self, **kwargs):
        from apps.payments.service import PaymentService

        self.payment = PaymentService.get_or_create_payment_for_sale(self)


class MultipleSateTransitions:
    workflow = MultipleSaleWorkflow()

    @transition(
        field="state",
        source=[
            workflow.DRAFT,
        ],
        target=workflow.GENERATED,
        permission="sales.can_send_to_payment",
        custom=dict(verbose="Confirmas compra"),
    )
    def create_sales(self, **kwargs):
        from apps.sales.services import SaleService

        SaleService.create_sales_from_multiple_sale(self)
