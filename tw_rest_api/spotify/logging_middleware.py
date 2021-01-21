from django.db import connection
from django.conf import settings
import logging


class LoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.response = None

    def __call__(self, request):
        response = self.get_response(request)
        self.response = response
        self.process_view(request, None, None, None)
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        logging.basicConfig(filename='logs.log', level=logging.INFO)

        if len(connection.queries) > 0 and settings.DEBUG:
            for query in connection.queries:
                nice_sql = query['sql'].replace('"', '').replace(',', ', ')
                logging.info(nice_sql)
