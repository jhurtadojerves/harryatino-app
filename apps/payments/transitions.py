"""Transitions for Project"""

from datetime import datetime

from django_fsm import transition
from environs import Env

# Services
from apps.payments.service import BaseService

# Local
from apps.workflows.exceptions import WorkflowException

from .workflows import PaymentWorkflow, PostWorkflow

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
        target=workflow.PAY,
        permission="payments.create_payment_post",
        custom=dict(verbose="Pagar"),
    )
    def to_pay(self, **kwargs):
        from apps.utils.services import APIService

        creatures_points = kwargs.get("creatures_points", 0)
        objects_points = kwargs.get("objects_points", 0)

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
            "customFields[33]": f"{context['creatures_points'] + creatures_points}",
            "customFields[34]": f"{context['objects_points'] + objects_points}",
        }

        APIService.update_user_profile(
            self.wizard.forum_user_id, raw_data=update_profile_data
        )
        self.html = html
        self.url = response_url

    @transition(
        field="state",
        source=[workflow.CREATED],
        target=workflow.CANCELED,
        permission="payments.create_payment_post",
        custom=dict(
            verbose="Cancelar", icon="fa-solid fa-ban", back_verbose="CANCELAR"
        ),
    )
    def to_cancel(self, **kwargs):
        pass

    def get_new_total(self, galleons):
        from apps.payments.choices import PaymentType

        if self.payment_type in PaymentType.get_plus_choices():
            return int(galleons + self.total_payments())
        return int(galleons - self.total_payments())

    def get_context(self, wizard):
        from apps.utils.services import APIService

        data = APIService.get_forum_user_data(wizard)
        old_galleons = int(data.get("customFields[12]")) or 0
        creatures_points = data.get("customFields[33]", 0)
        objects_points = data.get("customFields[34]", 0)

        context = {
            "payment": self,
            "old_galleons": old_galleons,
            "new_galleons": self.get_new_total(old_galleons),
            "creatures_points": int(creatures_points),
            "objects_points": int(objects_points),
        }

        return context

    def get_template(self):
        templates = {
            0: "payments/posts/magic_mall.html",
            1: "payments/posts/plus_equipo.html",
            2: "payments/posts/scholar_plus.html",
            3: "payments/posts/scholar_payment.html",
            4: "payments/posts/scholar_charge.html",
            5: "payments/posts/oros_to_galleons.html",
            6: "payments/posts/dungeons.html",
            99: "payments/posts/other_plus.html",
            100: "payments/posts/other_minus.html",
        }
        return templates.get(self.payment_type)
