from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from .models import Account
from .models import Emailer, PartCategory, Part, Assignment, Incoming


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


@admin.register(Part)
class PartAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'short_name', 'khs_id_field', 'khs_title_field')
    ordering = ('category__sort_order', 'sort_order', 'name')


@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = ('date', 'part', 'account', 'description')
    ordering = ('date', 'part__category__sort_order', 'part__sort_order')


@admin.register(Incoming)
class IncomingAdmin(admin.ModelAdmin):
    list_display = ('date', 'speaker_full_name', 'congregation_name', 'outline_name')
    ordering = ('date',)


@admin.register(Emailer)
class EmailerAdmin(admin.ModelAdmin):
    list_display = ('account', 'days_before')
    ordering = ('account', 'days_before')


admin.site.unregister(User)
admin.site.register(User, UserAdmin)

# Register your models here.
admin.site.register(PartCategory)
