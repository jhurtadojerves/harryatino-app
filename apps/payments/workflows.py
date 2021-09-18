# Local
from apps.workflows import WorkflowChoices, Workflow


class PostWorkflow(Workflow):
    class Choices(WorkflowChoices):
        CANCELED = 0, "Cancelado", dict(visible=False)
        CREATED = 1, "Creado"
        LOADED = 2, "Cargado"
        INDICTED = 3, "Procesado"
