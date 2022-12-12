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


class MonthlyPaymentWorkflow(Workflow):
    class Choices(WorkflowChoices):
        CANCELED = 0, "Cancelado", dict(visible=False)
        CREATED = 1, "Creado"
        CALCULATED = 2, "Calculado"
        PAY = 3, "Pagado"
        WITHOUT_PAY = 4, "Sin pago"
