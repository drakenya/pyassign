from django.core.management.base import BaseCommand

from ...models import Assignment
from ..loaders.loaders import KhsLoader, QassignLoader


class Command(BaseCommand):
    def handle(self, *args, **options):
        Assignment.objects.all().delete()

        QassignLoader.load()
        for endpoint in ['oclm']:
            KhsLoader.load(endpoint)
