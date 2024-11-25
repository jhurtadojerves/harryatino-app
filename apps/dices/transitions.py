"""Transitions for Sales"""

from django_fsm import transition

from apps.dices.workflows import TopicWorkflow
from apps.ecommerce.conditions import PurchaseConditions


class TopicTransitions:
    workflow = TopicWorkflow()

    @transition(
        field="state",
        source=[
            workflow.OPEN,
        ],
        target=workflow.CLOSED,
        permission="dices.can_manage",
        conditions=[
            PurchaseConditions.is_moderator,
        ],
        custom=dict(verbose="Cerrar Topic"),
    )
    def close(self, **kwargs):
        pass

    @transition(
        field="state",
        source=[
            workflow.CLOSED,
        ],
        target=workflow.OPEN,
        permission="dices.can_manage",
        conditions=[
            PurchaseConditions.is_moderator,
        ],
        custom=dict(verbose="Abrir Topic"),
    )
    def open(self, **kwargs):
        pass
