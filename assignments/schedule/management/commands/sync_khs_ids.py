import urllib.request
import json

from django.conf import settings
from django.core.management.base import BaseCommand

from ...models import Account


class Command(BaseCommand):
    def handle(self, *args, **options):
        for account in Account.objects.all():
            account.khsid = None
            account.save()

        response = urllib.request.urlopen(settings.API_ENDPOINTS['khsapi'] + 'names/')
        string_response = response.readall().decode('utf-8')
        data = json.loads(string_response)

        for item in data:
            try:
                found_account = Account.objects.get(user__first_name=item['first_name'], user__last_name=item['last_name'])
            except Account.DoesNotExist:
                pass
            else:
                found_account.khsid = item['id']
                found_account.save()
