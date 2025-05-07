from apps.workflows import Workflow, WorkflowChoices


class ProfileWorkflow(Workflow):
    class Choices(WorkflowChoices):
        CREATED = 1, "Creado"
