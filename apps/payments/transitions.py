from datetime import datetime

from django_fsm import RETURN_VALUE, transition
from environs import Env

from apps.ecommerce.conditions import PurchaseConditions
from apps.payments.service import BaseService, MonthlyPaymentService
from apps.workflows.exceptions import WorkflowException

from ..utils.services import TopicAPIService
from .workflows import (
    DonationWorkflow,
    MonthlyPaymentWorkflow,
    PaymentWorkflow,
    PostWorkflow,
)

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
        from apps.utils.services import TopicAPIService, UserAPIService

        creatures_points = kwargs.get("creatures_points", 0)
        objects_points = kwargs.get("objects_points", 0)

        vault = self.wizard.vault_number
        context = self.get_context(self.wizard)
        response, html = TopicAPIService.create_post(
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

        UserAPIService.update_user_profile(
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
        from apps.utils.services import UserAPIService

        data = UserAPIService.get_forum_user_data(wizard)
        old_galleons = int(data.get("customFields[12]")) or 0
        creatures_points = data.get("customFields[33]", 0)
        objects_points = data.get("customFields[34]", 0)

        if creatures_points == "":
            creatures_points = 0

        if objects_points == "":
            objects_points = 0

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


class MonthlyPaymentTransitions:
    workflow = MonthlyPaymentWorkflow()


class MonthlyLineTransitions:
    workflow = MonthlyPaymentWorkflow()

    @transition(
        field="state",
        source=[workflow.CREATED],
        target=RETURN_VALUE(workflow.PAY, workflow.WITHOUT_PAY),
        permission="payments.create_payment_post",
        custom=dict(verbose="Calcular", icon="fas fa-calculator"),
    )
    def to_pay(self, **kwargs):

        if not self.month.post_url:
            raise WorkflowException("Debes configurar la url de petición del descuento")

        total, monthly, galleons = MonthlyPaymentService.calculate_member_posts(
            self.month, self.work
        )
        MonthlyPaymentService.calculate_salary_scale(line=self, posts=total)
        calculated_value = MonthlyPaymentService.calculate_payment(
            line=self, posts=monthly, galleons=galleons
        )

        if calculated_value > 0:
            response, html = TopicAPIService.create_post(
                topic=self.work.wizard.vault_number,
                context={
                    "previous_galleons": galleons,
                    "url": self.month.post_url,
                    "reason": f"CMI {self.month.__str__()}",
                    "galleons": calculated_value,
                    "total_galleons": galleons + calculated_value,
                },
                template="payments/cmi.html",
            )
            self.paid_url = response["url"]

            return self.workflow.PAY
        else:
            return self.workflow.WITHOUT_PAY


class DonationTransitions:
    workflow = DonationWorkflow()

    @transition(
        field="state",
        source=[workflow.CREATED],
        target=workflow.CONFIRMED,
        permission="payments.view_donation",
        conditions=[
            PurchaseConditions.is_owner,
            PurchaseConditions.has_lines,
        ],
        custom=dict(verbose="Confirmar", icon="fas fa-check-double"),
    )
    def confirm(self, **kwargs):
        from apps.payments.service import DonationService

        DonationService.confirm(self)

    @transition(
        field="state",
        source=[workflow.CREATED],
        target=workflow.CANCELED,
        permission="payments.view_donation",
        conditions=[
            PurchaseConditions.is_owner,
        ],
        custom=dict(verbose="Cancelar", icon="fas fa-ban"),
    )
    def cancel(self, **kwargs):
        pass

    @transition(
        field="state",
        source=[workflow.CONFIRMED],
        target=workflow.APPROVED,
        permission="payments.can_approve_donation",
        custom=dict(verbose="Aprobar", icon="fas fa-check-double"),
    )
    def approve(self, **kwargs):
        from apps.payments.service import DonationService

        DonationService.approve(self)

    @transition(
        field="state",
        source=[workflow.CONFIRMED],
        target=workflow.REJECTED,
        permission="payments.can_reject_donation",
        custom=dict(verbose="Rechazar", icon="fas fa-ban"),
    )
    def reject(self, **kwargs):
        pass
