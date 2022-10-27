# DRF
from datetime import datetime, timedelta, timezone

from django.conf import settings
from rest_framework import exceptions
from rest_framework.serializers import ModelSerializer
from rest_framework.validators import UniqueTogetherValidator

from api.authentication.serializers.users import UserSerializer
from api.products.serializers import ProductSerializer
from apps.ecommerce.models import Purchase, PurchaseLine
from apps.ecommerce.workflows import PurchaseWorkflow
from config.middleware import GlobalRequestMiddleware


class PurchaseSerializer(ModelSerializer):
    user = UserSerializer

    class Meta:
        model = Purchase
        fields = ["id", "state", "user"]


class PurchaseLineSerializer(ModelSerializer):
    validators = [
        UniqueTogetherValidator(
            queryset=PurchaseLine.objects.all(),
            fields=["purchase", "product"],
            message="Ya tienes ese producto en tu carrito",
        )
    ]

    NOT_FOUND_EXCEPTION = exceptions.NotFound(
        {"purchase": "No pudimos encontrar tu carrito 🥺"}
    )

    class Meta:
        model = PurchaseLine
        fields = [
            "id",
            "purchase",
            "product",
        ]
        extra_kwargs = {"purchase": {"required": False, "allow_null": True}}

    def validate(self, data):
        request = GlobalRequestMiddleware.get_global_request()
        purchase = request.user.purchase()
        product = data.get("product", None)

        data.update({"purchase": purchase})

        self.check_purchase(purchase, request.user)
        self.check_product(product)
        self.validate_number_of_lines(purchase, product)

        return data

    @staticmethod
    def validate_number_of_lines(purchase, product):

        if purchase.lines.count() >= 8:  # Todo Check this validation, is more complex
            raise exceptions.ValidationError(
                {"purchase": "Tu carrito está lleno, no puedes añadir más 🥺"}
            )

        number_of_lines = (
            purchase.lines.filter(
                product__category__section__pk=product.category.section.pk
            )
            .distinct()
            .count()
        )

        if number_of_lines >= 2:
            raise exceptions.ValidationError(
                {
                    "purchase": f"La sección de {product.category.section} "
                    f"de tu carrito está llena, no puedes añadir más 🥺"
                }
            )

    def check_purchase(self, purchase, user):

        if not purchase:
            raise self.NOT_FOUND_EXCEPTION

        if purchase.state in [
            PurchaseWorkflow.Choices.CANCELED,
            PurchaseWorkflow.Choices.APPROVED,
        ]:
            raise self.NOT_FOUND_EXCEPTION

        purchases = (
            Purchase.objects.filter(state=Purchase.workflow.CONFIRMED, user=user)
            .exclude(id=purchase.id)
            .exists()
        )
        if purchases or purchase.state == PurchaseWorkflow.Choices.CONFIRMED:
            raise exceptions.ValidationError(
                {"purchase": "Tienes una compra pendiente de aprobación"}
            )

        last_purchase = Purchase.objects.filter(
            state=PurchaseWorkflow.Choices.APPROVED, user=user
        ).last()

        if last_purchase:
            seconds = (
                datetime.now(timezone.utc) - last_purchase.confirm_date
            ).total_seconds()
            valid_time = seconds > settings.CHECKOUT_COOLDOWN_HOURS * 3600

            if not valid_time:
                seconds_wait = settings.CHECKOUT_COOLDOWN_HOURS * 3600 - seconds
                seconds_wait = int(seconds_wait)
                message = str(timedelta(seconds=seconds_wait))
                raise exceptions.ValidationError(
                    {"purchase": f"Para realizar otra compra debes esperar {message}"}
                )

    def check_product(self, product):
        if not product:
            raise self.NOT_FOUND_EXCEPTION

        if not product.can_be_sold:
            raise exceptions.ValidationError(
                {"product": f"El producto {product} no se puede vender 🥺"},
            )

        if product.available_stock <= 0:
            raise exceptions.ValidationError(
                {"product": f"El producto {product} no tiene stock 🥺"}
            )


class PurchaseLineSerializerReturn(ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = PurchaseLine
        fields = [
            "product",
        ]
