from tracing.middleware import TracingMiddleware


class PurchaseConditions:
    @classmethod
    def is_owner(cls, instance):
        information = TracingMiddleware.get_info()
        user = information.get("user", False)

        if not user or not user.is_authenticated:
            return False

        return instance.user == user

    @classmethod
    def has_lines(cls, instance):
        return instance.lines.count() > 0

    @classmethod
    def is_moderator(cls, instance):
        information = TracingMiddleware.get_info()
        user = information.get("user", False)

        if not user or not user.is_authenticated:
            return False

        if not user.is_moderator and not user.is_superuser:
            return False

        return True
