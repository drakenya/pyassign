import urllib.request

from django.conf import settings

from ...models import Assignment, Incoming
from ..loaders.loaders import IncomingLoader, KhsLoader, QassignLoader


class LoadController:
    @classmethod
    def load_all(cls):
        # Force update on all API endpoints
        cls._update_endpoints()

        # Clear current db cache
        cls._update_endpoints()

        # Load all
        cls._update_data_from_endpoints()


    @staticmethod
    def _update_endpoints():
        request_data = "".encode('ascii')
        update_endpoints = [
            settings.API_ENDPOINTS['khsapi'] + 'update/',
            settings.API_ENDPOINTS['qassigns'] + 'update/',
        ]
        for endpoint in update_endpoints:
            request = urllib.request.Request(endpoint, request_data)
            urllib.request.urlopen(request)

    @staticmethod
    def _clear_db_cache():
        Assignment.objects.all().delete()
        Incoming.objects.all().delete()


    @staticmethod
    def _update_data_from_endpoints():
        QassignLoader.load()
        for endpoint in ['oclm', 'sound', 'schedule', 'outgoing/all']:
            KhsLoader.load(endpoint)
        IncomingLoader.load()