"""Mixin from app"""

# Django
from django.shortcuts import redirect, reverse
from django.http import HttpResponsePermanentRedirect

# Local
from ..menu.utils import get_site_url


class AnnouncementListMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        if self.model.objects.all().exists():
            context.update({"last": self.model.objects.first()})
        return context

    def get(self, request, *args, **kwargs):
        if self.model.objects.all().exists():
            return HttpResponsePermanentRedirect(
                reverse(get_site_url(self.model.objects.first(), "detail"))
            )

        return super(AnnouncementListMixin, self).get(request, *args, **kwargs)


class AnnouncementDetailMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context.update({"announcements": self.model.objects.all()})
        return context
