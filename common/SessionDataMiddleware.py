from importlib import import_module

from django.conf import settings
from django.utils.deprecation import MiddlewareMixin


class SessionDataMiddleware(MiddlewareMixin):
    def __init__(self, get_response=None):
        self.get_response = get_response
        engine = import_module(settings.SESSION_ENGINE)
        self.SessionStore = engine.SessionStore

    def process_request(self, request):
        session_key = request.META.get('HTTP_SESSIONID', None)
        request.session = self.SessionStore(session_key)
