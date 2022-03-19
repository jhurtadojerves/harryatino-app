"""Mixins for utils models"""

# Django
from django.shortcuts import redirect

# Third party integration
from superadmin.templatetags.superadmin_utils import site_url


class LinkDetailMixin:
    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return redirect(site_url(self.object, "detail"))
