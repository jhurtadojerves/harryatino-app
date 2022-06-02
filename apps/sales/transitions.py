"""Transitions for Sales"""
# Third party integration
from django_fsm import transition

# Local
from apps.sales.workflows import SaleWorkflow


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
