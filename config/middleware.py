import threading


class GlobalRequestMiddleware(object):
    thread_local = threading.local()

    def __init__(self, get_response):
        self.get_response = get_response

    @classmethod
    def get_global_request(cls):
        return cls.thread_local.global_request

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called
        self.thread_local.global_request = request
        response = self.get_response(request)
        return response
