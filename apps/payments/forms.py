# Django
from django import forms
from django.forms import inlineformset_factory

# Third party integration
from django_select2.forms import (
    ModelSelect2Widget,
    ModelSelect2MultipleWidget,
)
from superadmin.forms import ModelForm

# Local
from apps.payments.models import Work, Payment, PaymentLine


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
        fieldsets = ("wizard",)
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
