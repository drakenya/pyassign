from django.core.management.base import BaseCommand

from ..loaders.controller import LoadController


class Command(BaseCommand):
    def handle(self, *args, **options):
        LoadController.load_all()

