# Third party integration
from superadmin.decorators import register

# Base
from apps.ecommerce.mixins import PurchaseDetailMixin, PurchaseListMixin
from config.model_site import DefaultSite


@register("ecommerce.Purchase")
class PurchaseSite(DefaultSite):
    allow_views = ("list", "detail")
    url_detail_suffix = None

    list_mixins = [PurchaseListMixin]
    detail_mixins = [PurchaseDetailMixin]

    detail_template_name = None
    list_template_name = None

    detail_fields = {
        "Detalle de usuario": [
            ["user__profile:Perfil", "user__profile__galleons", "user"]
        ],
        "Detalle de la Compra": [
            ["confirm_date"],
            ["purchase_url", "certification_url", "discount_url"],
        ],
    }
