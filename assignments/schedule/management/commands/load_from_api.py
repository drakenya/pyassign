from django.core.management.base import BaseCommand

from ...models import Assignment, Incoming
from ..loaders.loaders import IncomingLoader, KhsLoader, QassignLoader


class Command(BaseCommand):
    def handle(self, *args, **options):
        Assignment.objects.all().delete()
        Incoming.objects.all().delete()

        QassignLoader.load()
        for endpoint in ['oclm', 'sound', 'schedule', 'outgoing/all']:
            KhsLoader.load(endpoint)
        IncomingLoader.load()
