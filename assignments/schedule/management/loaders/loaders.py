import urllib.request
import json

from django.conf import settings

from ..cache import cache
from ...models import Assignment, Part


class QassignLoader:
    @staticmethod
    def load():
        response = urllib.request.urlopen(settings.API_ENDPOINTS['qassigns'])
        string_response = response.readall().decode('utf-8')
        data = json.loads(string_response)

        part_cache = cache.LookupCache(cache.PartCacheLookup)
        initial_cache = cache.LookupCache(cache.InitialCacheLookup)

        for item in data:
            date, part_code, initials = item['date'], item['part_code'], item['initials']
            part_id = part_cache[part_code]
            initials_id = initial_cache[initials]

            if part_id and initials_id:
                assignment = Assignment(date=date, part_id=part_id, account_id=initials_id)
                assignment.save()


class KhsLoader:
    @staticmethod
    def load(khs_prefix):
        if khs_prefix[-1:] is not '/':
            khs_prefix += '/'

        response = urllib.request.urlopen(settings.API_ENDPOINTS['khsapi'] + khs_prefix)
        string_response = response.readall().decode('utf-8')
        data = json.loads(string_response)

        account_cache = cache.LookupCache(cache.AccountCacheLookup)
        findable_parts = Part.objects.all().filter(khs_id_field__startswith=khs_prefix)

        for item in data:
            date = item['date']

            for findable in findable_parts:
                key = findable.khs_id_field[len(khs_prefix):]
                if item[key] is not None and account_cache[item[key]] is not None:
                    account_id = account_cache[item[key]]
                    assignment = Assignment(date=date, part=findable, account_id=account_id)
                    assignment.save()
