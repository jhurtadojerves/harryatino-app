"""Transitions for Sales"""


from django_fsm import transition

from apps.sales.workflows import MultipleSaleWorkflow, SaleWorkflow


class SaleTransitions:
    workflow = SaleWorkflow()

    @transition(
        field="state",
        source=[
            workflow.CREATED,
        ],
        target=workflow.PAY,
        permission="sales.can_send_to_payment",
        custom=dict(verbose="Enviar a Pago"),
    )
    def send_to_pay(self, **kwargs):
        from apps.payments.service import PaymentService

        self.payment = PaymentService.get_or_create_payment_for_sale(self)


class MultipleSateTransitions:
    workflow = MultipleSaleWorkflow()

    @transition(
        field="state",
        source=[
            workflow.DRAFT,
        ],
        target=workflow.GENERATED,
        permission="sales.can_send_to_payment",
        custom=dict(verbose="Confirmas compra"),
    )
    def create_sales(self, **kwargs):
        from apps.sales.services import SaleService
        from apps.utils.services import UserAPIService

        SaleService.create_sales_from_multiple_sale(self)

        profile = UserAPIService.download_user_data_and_update(self.profile)
        data = UserAPIService.get_forum_user_data(profile)
        creatures_points = data.get("customFields[33]", 0)
        objects_points = data.get("customFields[34]", 0)

        creatures_points = int(creatures_points) if creatures_points != "" else 0
        objects_points = int(objects_points) if objects_points != "" else 0

        update_profile_data = {
            "customFields[33]": creatures_points + self.get_creatures_points_sales,
            "customFields[34]": objects_points + self.get_objects_points_sales,
        }

        UserAPIService.update_user_profile(
            profile.forum_user_id, raw_data=update_profile_data
        )
