"""Transitions for Project"""
# Django
from django.core.exceptions import ObjectDoesNotExist

# Python
from datetime import datetime

# Third party integration
from apps import workflows
from apps.workflows import exceptions
from django_fsm import transition

# Local
from apps.workflows.exceptions import WorkflowException
from .workflows import PostWorkflow

# Services
from .service import BaseService


class PostTransitions:
    workflow = PostWorkflow()

    @transition(
        field="state",
        source=[
            workflow.CREATED,
        ],
        target=workflow.LOADED,
        custom=dict(verbose="Cargar posts"),
    )
    def to_load(self, **kwargs):
        initial_date = datetime.now()
        print(initial_date)
        print("Comenzando...")
        try:
            self.content = BaseService.get_posts(per_page=500)
        except Exception as error:
            raise WorkflowException(str(error))
        print("Terminado")
        end_date = datetime.now()
        print(end_date)
        print(end_date - initial_date)

    @transition(
        field="state",
        source=[
            workflow.LOADED,
            workflow.INDICTED,
        ],
        target=workflow.INDICTED,
        custom=dict(verbose="Procesar posts"),
    )
    def to_indict(self, **kwargs):
        initial_date = datetime.now()
        print(initial_date)
        print("Comenzando...")
        try:
            self.parse_content = BaseService.calculate_all_posts(self.content)
        except Exception as error:
            raise WorkflowException(str(error))
        print("Terminado")
        end_date = datetime.now()
        print(end_date)
        print(end_date - initial_date)
