from django.forms import HiddenInput, inlineformset_factory
from django_select2.forms import ModelSelect2Widget
from superadmin.forms import ModelForm

from apps.payments.models import Payment, PaymentLine, Work
from apps.payments.models.donations import Donation, DonationLine


class WorkMonthForm(ModelForm):
    class Meta:
        model = Work
        fieldsets = ("is_active", "wizard", "work", "work_description")
        widgets = {
            "wizard": ModelSelect2Widget(
                model="profiles.Profile",
                search_fields=["nick__unaccent__icontains", "forum_user_id__icontains"],
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
                search_fields=["nick__unaccent__icontains", "forum_user_id__icontains"],
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


class DonationForm(ModelForm):
    class Meta:
        model = Donation
        fields = ("user",)
        widgets = {"user": HiddenInput()}

    def __init__(self, *args, **kwargs):
        super(DonationForm, self).__init__(*args, **kwargs)
        self.fields["user"].required = False


class DonationLineForm(ModelForm):
    class Meta:
        model = DonationLine
        fields = ("beneficiary", "quantity", "reason")
        widgets = {
            "beneficiary": ModelSelect2Widget(
                model="profiles.Profile",
                search_fields=["nick__unaccent__icontains", "forum_user_id__icontains"],
                attrs={
                    "data-minimum-input-length": 0,
                },
            ),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super(DonationLineForm, self).__init__(*args, **kwargs)

        if user and hasattr(user, "profile"):
            self.fields["beneficiary"].queryset = self.fields[
                "beneficiary"
            ].queryset.exclude(id=user.profile.id)


class DonationLineEdit(ModelForm):
    class Meta:
        model = DonationLine
        fields = ("quantity", "reason")
        widgets = {
            "beneficiary": ModelSelect2Widget(
                model="profiles.Profile",
                search_fields=["nick__unaccent__icontains", "forum_user_id__icontains"],
                attrs={
                    "data-minimum-input-length": 0,
                },
            ),
        }


PaymentLineFormset = inlineformset_factory(
    Payment,
    PaymentLine,
    form=PaymentLineForm,
    min_num=1,
    validate_min=True,
)

DonationLineFormset = inlineformset_factory(
    Donation,
    DonationLine,
    form=DonationLineForm,
    min_num=1,
    validate_min=True,
    max_num=2,
    can_delete=False,
)
