from apps.workflows import Workflow, WorkflowChoices


class UpdateLevelWorkflow(Workflow):
    class Choices(WorkflowChoices):
        DRAFT = 1, "Borrador"
        DONE = 2, "Completado"
