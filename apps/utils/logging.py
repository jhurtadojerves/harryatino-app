from apps.utils.middlewares import RequestIDMiddleware


class RequestIDLogFilter:
    def filter(self, record):
        record.request_id = RequestIDMiddleware.get_request_id() or "-"

        return True
