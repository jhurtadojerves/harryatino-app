from tracing.middleware import TracingMiddleware


class ManagementConditions:
    @classmethod
    def not_done(cls, instance):
        return not instance.is_done

    @classmethod
    def can_update_levels(cls, instance):
        information = TracingMiddleware.get_info()
        user = information.get("user", False)

        if not user or not user.is_authenticated:
            return False

        return user.is_superuser or user.has_perm("management.can_update_levels")
