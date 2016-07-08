from collections import defaultdict

from ...models import Account, Part


class LookupCache(defaultdict):
    def __init__(self, lookup_device):
        super().__init__()
        self._lookup_device = lookup_device

    def __missing__(self, key):
        self[key] = self._lookup_device.lookup(key)
        return self[key]

    def get_undefined_keys(self):
        return sorted([key for key in self.keys() if self[key] is None])


class PartCacheLookup:
    @staticmethod
    def lookup(key):
        try:
            part = Part.objects.get(short_name=key.lower())
            return part.id
        except Part.DoesNotExist:
            return None


class InitialCacheLookup:
    @staticmethod
    def lookup(key):
        try:
            account = Account.objects.get(initials=key.lower())
            return account.id
        except Account.DoesNotExist:
            return None


class AccountCacheLookup:
    @staticmethod
    def lookup(key):
        try:
            account = Account.objects.get(khsid=key)
            return account.id
        except Account.DoesNotExist:
            return None