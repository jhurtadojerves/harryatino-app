from tracing.middleware import TracingMiddleware


class ManagementConditions:
    @classmethod
    def not_done(cls, instance):
        return not instance.level_update.state == 2

    @classmethod
    def is_admin(cls, instance):
        information = TracingMiddleware.get_info()
        user = information.get("user", False)

        if not user:
            return False

        if not user.is_superuser:
            return False

        return True
