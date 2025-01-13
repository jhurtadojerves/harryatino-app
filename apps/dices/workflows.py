from apps.workflows import Workflow, WorkflowChoices


class TopicWorkflow(Workflow):
    class Choices(WorkflowChoices):
        CLOSED = 0, "Cerrado", dict(visible=False)
        OPEN = 1, "Abierto"
        HIDDEN = 2, "Oculto", dict(visible=False)
