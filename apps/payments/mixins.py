from django.db.models import CharField, Q
from django.db.models.functions import Cast
from django.shortcuts import redirect

from apps.payments.choices import PaymentType
from apps.payments.forms import DonationLineForm
from apps.payments.models.donations import Donation
from apps.payments.service import DonationService
from apps.payments.workflows import DonationWorkflow
from config.mixins.filteriing import FilterByChoice


class WorkListMixin:
    def get_queryset(self):
        search = self.request.GET.get("search", False)
        queryset = super().get_queryset()
        if search:
            queryset = queryset.filter(
                Q(wizard__nick__unaccent__icontains=search)
                | Q(wizard__forum_user_id__icontains=search)
            )
        return queryset


class PaymentListMixin(FilterByChoice):
    CHOICES = PaymentType.choices
    SEARCH_PARAM = "payment_type"

    def get_queryset(self):
        queryset = super().get_queryset()
        choice_param = self.request.GET.get("choice_param", None)
        search = self.request.GET.get("search", False)

        if choice_param:
            search_choice = self.get_search_selected_choice(choice_param)

            if type(search_choice) == int:  # noqa: E721
                queryset = queryset.filter(payment_type=search_choice)

        if search:
            queryset = queryset.filter(
                Q(wizard__nick__unaccent__icontains=search)
                | Q(wizard__forum_user_id__icontains=search)
            )

        return queryset


class DonationFormMixin:
    def get(self, request, *args, **kwargs):
        DonationService.validate_donation(request)
        exists_redirect = DonationService.get_redirect(request)

        if exists_redirect:
            return redirect(exists_redirect)

        donation = Donation.objects.create(user=request.user)
        self.object = donation

        return redirect(self.get_success_url())


class DonationDetailMixin:
    form_class = DonationLineForm


class DonationListMixin(FilterByChoice):
    CHOICES = DonationWorkflow.Choices.choices
    SEARCH_PARAM = "state"

    def get_queryset(self):
        queryset = super().get_queryset()
        search = self.request.GET.get("search", False)
        user = self.request.user
        perms_list = ["payments.can_approve_donation", "payments.can_reject_donation"]
        perms = [user.has_perm(perm) for perm in perms_list]

        if not user.is_authenticated:
            return queryset.none()

        if not any(perms):
            queryset = queryset.filter(Q(user=user) | Q(lines__beneficiary__user=user))

        if search:
            queryset = queryset.annotate(
                forum_user_id_str=Cast("user__profile__forum_user_id", CharField())
            ).filter(
                Q(user__profile__nick__unaccent__icontains=search)
                | Q(forum_user_id_str__icontains=search)
            )

        return queryset
