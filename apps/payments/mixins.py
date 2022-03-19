"""Mixins for work site"""
# Django
from django.db.models import Q
from django.shortcuts import redirect


class WorkListMixin:
    def get_queryset(self):
        search = self.request.GET.get("search", False)
        queryset = super().get_queryset()
        if search:
            queryset = queryset.filter(
                Q(wizard__nick__icontains=search)
                | Q(wizard__forum_user_id__icontains=search)
            )
        return queryset


"""
class PaymentFormMixin:
    def form_valid(self, form):
        self.object = form.save(commit=False)
        return redirect(self.get_success_url())
"""
