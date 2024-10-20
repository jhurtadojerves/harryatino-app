from django_fsm import transition

from apps.products.workflows import StockTransactionWorkflow


class StockRequestTransitions:
    workflow = StockTransactionWorkflow()

    @transition(
        field="state",
        source=[
            workflow.CREATED,
        ],
        target=workflow.APPROVED,
        permission="products.can_approve",
        custom=dict(verbose="Aprobar"),
    )
    def approve(self, **kwargs):
        products = self.product_requests.all()

        for product in products:
            product.product.stock += product.requested_amount
            product.product.save()
    
    @transition(
        field="state",
        source=[
            workflow.CREATED,
        ],
        target=workflow.REJECTED,
        permission="products.can_approve",
        custom=dict(verbose="Rechazar"),
    )
    def reject(self, **kwargs):
        pass


    @transition(
        field="state",
        source=[
            workflow.CREATED,
        ],
        target=workflow.CANCELED,
        custom=dict(verbose="Cancelar"),
    )
    def cancel(self, **kwargs):
        pass

    @transition(
        field="state",
        source=[
            workflow.APPROVED,
        ],
        target=workflow.ANNULLED,
        permission="products.can_approve",
        custom=dict(verbose="Rechazar"),
    )
    def annul(self, **kwargs):
        products = self.product_requests.all()

        for product in products:
            new_stock = max(0, product.product.stock - product.requested_amount)
            product.product.stock = new_stock
            product.product.save()
