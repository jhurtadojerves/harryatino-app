import threading


class GlobalRequestMiddleware(object):
    thread_local = threading.local()

    def __init__(self, get_response):
        self.get_response = get_response

    @classmethod
    def get_global_request(cls):
        return cls.thread_local.global_request

    @staticmethod
    def get_or_create_checkout(user):
        if user.is_authenticated:
            from apps.ecommerce.models import Purchase

            choices = [
                Purchase.workflow.Choices.CREATED,
                Purchase.workflow.Choices.CONFIRMED,
            ]

            checkout_exists = Purchase.objects.filter(
                user=user,
                state__in=choices,
            ).exists()

            if not checkout_exists:
                Purchase.objects.create(user=user)

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called
        self.thread_local.global_request = request
        self.get_or_create_checkout(request.user)
        response = self.get_response(request)
        return response
