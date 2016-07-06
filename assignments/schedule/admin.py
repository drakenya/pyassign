from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from .models import Account
from .models import PartCategory, Part, Assignment


# User/Account
class AccountInline(admin.StackedInline):
    model = Account
    can_delete = False


# New user admin
class UserAdmin(BaseUserAdmin):
    inlines = (AccountInline, )
    list_display = ('username', 'first_name', 'last_name', 'is_active', 'account_initials', 'account_khsid')

    def account_initials(self, admin):
        return admin.account.initials
    account_initials.short_description = 'Initials'

    def account_khsid(self, admin):
        return admin.account.khsid
    account_khsid.short_description = 'KHS ID'



admin.site.unregister(User)
admin.site.register(User, UserAdmin)

# Register your models here.
admin.site.register(PartCategory)
admin.site.register(Part)
admin.site.register(Assignment)