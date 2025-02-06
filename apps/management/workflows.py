from apps.workflows import Workflow, WorkflowChoices


class UpdateLevelWorkflow(Workflow):
    class Choices(WorkflowChoices):
        DRAFT = 1, "En curso"
        DONE = 2, "Completado"


class UpdateLevelLineWorkflow(Workflow):
    class Choices(WorkflowChoices):
        DRAFT = 1, "En curso"
        DONE = 2, "Completado"
        CANCELED = 3, "Completado"
