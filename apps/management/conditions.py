from tracing.middleware import TracingMiddleware


class ManagementConditions:
    @classmethod
    def not_done(cls, instance):
        return not instance.is_done

    @classmethod
    def is_admin(cls, instance):
        information = TracingMiddleware.get_info()
        user = information.get("user", False)

        if not user or not user.is_authenticated:
            return False

        if not user.is_superuser:
            return False

        return True
