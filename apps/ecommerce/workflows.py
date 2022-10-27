from django.db import models

# Local
from apps.workflows import Workflow, WorkflowChoices


class PurchaseWorkflow(Workflow):
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


class PurchaseWorkflowChoices(models.IntegerChoices):
    CANCELED = (
        0,
        "Cancelado",
    )
    CREATED = (
        1,
        "Creado",
    )
    CONFIRMED = (
        2,
        "Confirmado",
    )
    APPROVED = (
        3,
        "Aprobado",
    )
    REJECTED = 4, "Rechazada"
