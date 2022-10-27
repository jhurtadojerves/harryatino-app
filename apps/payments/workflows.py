# Local
from apps.workflows import Workflow, WorkflowChoices


class PostWorkflow(Workflow):
    class Choices(WorkflowChoices):
        CANCELED = 0, "Cancelado", dict(visible=False)
        CREATED = 1, "Creado"
        LOADED = 2, "Cargado"
        INDICTED = 3, "Procesado"


class PaymentWorkflow(Workflow):
    class Choices(WorkflowChoices):
        CANCELED = 0, "Cancelado", dict(visible=False)
        CREATED = 1, "Creado"
        PAY = 2, "Pagado"
