# Local
from apps.workflows import Workflow, WorkflowChoices


class SaleWorkflow(Workflow):
    class Choices(WorkflowChoices):
        CANCELED = 0, "Cancelado", dict(visible=False)
        CREATED = 1, "Creado"
        PAY = 2, "Pagado"


class MultipleSaleWorkflow(Workflow):
    class Choices(WorkflowChoices):
        CANCELED = 0, "Cancelado", dict(visible=False)
        DRAFT = 1, "Borrador"
        GENERATED = 2, "Generado"
