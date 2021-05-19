"""Mixin to dynamic forms app"""


class ActionDetailMixin:
    def has_permission(self):
        self.object = self.get_object()
        if self.object.super_admin_required and not self.request.user.is_superuser:
            return False
        return super().has_permission()
