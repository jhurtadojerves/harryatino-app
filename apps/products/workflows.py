from apps.workflows import Workflow, WorkflowChoices


class StockTransactionWorkflow(Workflow):
    class Choices(WorkflowChoices):
        CANCELED = 0, "Cancelado", dict(visible=False)
        CREATED = 1, "Creado"
        APPROVED = 2, "Aprobado"
        ANNULLED = (
            3,
            "Anulado",
            dict(
                icon="ki ki-bold-close",
                background="#ff9994",
                color="#ff392e",
                visible=False,
            ),
        )
        REJECTED = (
            4,
            "Rechazado",
            dict(
                icon="ki ki-bold-close",
                background="#ff9994",
                color="#ff392e",
                visible=False,
            ),
        )
