"""Mixins for utils models"""

from django.shortcuts import redirect


class LinkDetailMixin:
    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return redirect(self.object.destination)
