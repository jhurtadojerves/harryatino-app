# Local
from apps.workflows import WorkflowChoices, Workflow


class SaleWorkflow(Workflow):
    class Choices(WorkflowChoices):
        CANCELED = 0, "Cancelado", dict(visible=False)
        CREATED = 1, "Creado"
        PAY = 2, "Pagado"
