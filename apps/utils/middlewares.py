import threading
import uuid

from django.urls.resolvers import ResolverMatch
from newrelic import agent


class RequestIDMiddleware:
    _local = threading.local()

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request_id = request.headers.get("X-Request-ID") or str(uuid.uuid4())
        request.request_id = request_id
        self._local.request_id = request_id
        response = self.get_response(request)
        response["X-Request-ID"] = request.request_id

        if hasattr(self._local, "request_id"):
            del self._local.request_id

        return response

    @staticmethod
    def get_request_id():
        return getattr(RequestIDMiddleware._local, "request_id", None)


class NewRelicTrackingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if hasattr(request, "user") and request.user.is_authenticated:
            agent.add_custom_parameter("user_id", request.user.id)
            agent.add_custom_parameter("username", request.user.username)

        if hasattr(request, "request_id"):
            agent.add_custom_parameter("request_id", request.request_id)

        response = self.get_response(request)
        resolver_match: ResolverMatch = getattr(request, "resolver_match", None)

        if resolver_match:
            route = resolver_match.route
            transaction_name = f"{request.method} {route}"
            agent.add_custom_parameter("path", route)
            agent.set_transaction_name(transaction_name)

        return response
