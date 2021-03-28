"""Mixins for super admin"""

# Django
from django.contrib.auth.mixins import (
    PermissionRequiredMixin as DjangoPermissionRequiredMixin,
)


class NotPermissionRequiredMixin(DjangoPermissionRequiredMixin):
    """Verify model access permissions"""

    def has_permission(self):
        return True
