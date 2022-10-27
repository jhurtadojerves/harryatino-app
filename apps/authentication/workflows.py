# Local
from apps.workflows import Workflow, WorkflowChoices


class UserTokenWorkflow(Workflow):
    class Choices(WorkflowChoices):
        CANCELED = 0, "Cancelado", dict(visible=False)
        SEND = 1, "Enviado"
