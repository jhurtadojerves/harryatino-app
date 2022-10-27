"""Transitions for Sales"""
# Third party integration
from django_fsm import transition

# Local
from apps.authentication.workflows import UserTokenWorkflow


class UserTokenTransitions:
    workflow = UserTokenWorkflow()

    @transition(
        field="state",
        source=[
            workflow.SEND,
        ],
        target=workflow.SEND,
        permission="authentication.change_accesstoken",
        custom=dict(verbose="Volver a enviar MP"),
    )
    def send(self, **kwargs):
        self.send_message()
