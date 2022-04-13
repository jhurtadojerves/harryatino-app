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
from apps.payments.service import BaseService
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
        source=[workflow.CREATED],
        target=workflow.CANCELED,
        permission="payments.create_payment_post",
        custom=dict(verbose="Cancelar"),
    )
    def to_cancel(self, **kwargs):
        pass

    @transition(
        field="state",
        source=[workflow.CREATED],
        target=workflow.PAY,
        permission="payments.create_payment_post",
        custom=dict(verbose="Pagar"),
    )
    def to_pay(self, **kwargs):
        from apps.utils.services import APIService

        vault = self.wizard.vault_number
        context = self.get_context(self.wizard)
        response, html = APIService.create_post(
            topic=vault,
            context=context,
            template=self.get_template(),
        )
        response_url = response["url"]
        update_profile_data = {
            "customFields[12]": f"{context['new_galleons']}",
        }
        APIService.update_user_profile(
            self.wizard.forum_user_id, raw_data=update_profile_data
        )
        self.html = html
        self.url = response_url

    def get_context(self, wizard):
        from apps.utils.services import APIService

        data = APIService.get_forum_user_data(wizard)
        old_galleons = int(data.get("customFields[12]")) or 0
        if self.payment_type == 0:
            new_galleons = int(old_galleons - self.total_payments())
        elif self.payment_type == 1:
            new_galleons = int(old_galleons + self.total_payments())
        else:
            new_galleons = int(old_galleons + self.total_payments())

        context = {
            "payment": self,
            "old_galleons": old_galleons,
            "new_galleons": new_galleons,
        }

        return context

    def get_template(self):
        templates = {
            0: "payments/posts/magic_mall.html",
            1: "payments/posts/plus_equipo.html",
        }
        return templates.get(self.payment_type)
