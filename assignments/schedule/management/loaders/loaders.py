import urllib.request
import json

from django.conf import settings

from ..cache import cache
from ...models import Assignment


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