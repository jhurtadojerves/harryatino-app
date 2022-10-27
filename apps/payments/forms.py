# Django
from django.forms import inlineformset_factory

# Third party integration
from django_select2.forms import ModelSelect2Widget
from superadmin.forms import ModelForm

# Local
from apps.payments.models import Payment, PaymentLine, Work


class WorkMonthForm(ModelForm):
    class Meta:
        model = Work
        fieldsets = ("is_active", "wizard", "work", "work_description")
        widgets = {
            "wizard": ModelSelect2Widget(
                model="profiles.Profile",
                search_fields=["nick__icontains", "forum_user_id__icontains"],
                attrs={
                    "data-minimum-input-length": 0,
                },
            ),
        }


class PaymentForm(ModelForm):
    class Meta:
        model = Payment
        fieldsets = (("wizard", "payment_type"),)
        widgets = {
            "wizard": ModelSelect2Widget(
                model="profiles.Profile",
                search_fields=["nick__icontains", "forum_user_id__icontains"],
                attrs={
                    "data-minimum-input-length": 0,
                },
            ),
        }


class PaymentLineForm(ModelForm):
    class Meta:
        model = PaymentLine
        fields = (
            "amount",
            "verbose",
            "link",
        )


PaymentLineFormset = inlineformset_factory(
    Payment,
    PaymentLine,
    form=PaymentLineForm,
    min_num=1,
    validate_min=True,
)
