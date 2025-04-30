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


class DonationWorkflow(Workflow):
    class Choices(WorkflowChoices):
        CANCELED = 0, "Cancelado", dict(visible=False)
        CREATED = 1, "Creado"
        CONFIRMED = 2, "Confirmado"
        APPROVED = 3, "Aprobado"
        REJECTED = (
            4,
            "Rechazada",
            dict(
                icon="ki ki-bold-close",
                background="#ff9994",
                color="#ff392e",
                visible=False,
            ),
        )
