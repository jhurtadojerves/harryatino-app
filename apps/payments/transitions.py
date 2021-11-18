"""Transitions for Project"""
# Django
from django.core.exceptions import ObjectDoesNotExist

# Python
from datetime import datetime

# Third party integration
from apps import workflows
from apps.workflows import exceptions
from django_fsm import transition
import requests
from environs import Env

# Local
from apps.workflows.exceptions import WorkflowException
from .workflows import PostWorkflow, PaymentWorkflow

# Services
from .service import BaseService
from config.utils import get_short_url

env = Env()
API_KEY = env("API_KEY")


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


class PaymentTransitions:
    workflow = PaymentWorkflow()

    @transition(
        field="state",
        source=[
            workflow.CREATED,
        ],
        target=workflow.PAY,
        custom=dict(verbose="Pagar"),
    )
    def to_pay(self, **kwargs):
        for line in self.lines.all():
            if line.link:
                data = get_short_url(line.link)
                line.short_link = data.get("link", False)
                line.save()

    def create_post(self, request, previous_galleons, topic):
        galleons = self.object.calculated_value
        html = self.post_html(
            data={
                "previous_galleons": previous_galleons,
                "url": self.object.month.post_url,
                "reason": f"CMI {self.object.month.__str__()}",
                "galleons": galleons,
                "total_galleons": galleons + previous_galleons,
            },
        )
        # author = request.user.profile.forum_user_id
        author = 121976
        payload = f"topic={topic}&author={author}&post={html}"
        url = f"https://www.harrylatino.org/api/forums/posts?key={API_KEY}"
        response = self.post_request(url, payload)
        return response.json()
