"""Mixins for work site"""
# Django
from django.db.models import Q


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
