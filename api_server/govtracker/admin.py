from django.contrib import admin
from models import GovFinAccount, GovFinSubaccount, GovFinLedger


class GovFinAccountAdmin(admin.ModelAdmin):
    search_fields = ('name', 'shortname')
    list_display = ('name',)
    actions = []

    def has_add_permission(self, request, obj=None):
        return False

    def get_actions(self, request):
        return []

    def get_list_display_links(self, request, list_display):
        return None

    def has_delete_permission(self, request, obj=None):
        return False

    def save_model(self, request, obj, form, change):
        raise Exception('changes to financial accounts are not allowed')

    def get_queryset(self, request):
        return super(GovFinAccountAdmin, self).get_queryset(request).order_by('name')

    def delete_model(self, request, obj):
        raise Exception('delete on this model is not permitted.')


class GovFinSubaccountAdmin(admin.ModelAdmin):
    search_fields = ('name', 'shortname')
    list_display = ('acctid', 'created', 'name', 'allocationamt', 'closedby', 'closedat')
    list_filter = ('acctid',)
    list_editable = ('allocationamt',)
    actions = []

    def get_readonly_fields(self, request, obj=None):
        all_readonly = ['created', 'byuser', 'isallocation', 'closedby', 'closedat']
        if obj:
            return all_readonly + ['acctid', 'name', 'shortname']
        return all_readonly

    def has_add_permission(self, request, obj=None):
        return False

    def get_actions(self, request):
        return []

    def get_list_display_links(self, request, list_display):
        return ['name']

    def has_delete_permission(self, request, obj=None):
        return False

    def save_model(self, request, obj, form, change):
        raise Exception('changes to financial subaccounts are not allowed')

    def get_queryset(self, request):
        return super(GovFinSubaccountAdmin, self).get_queryset(request).order_by('-created')

    def delete_model(self, request, obj):
        raise Exception('delete on this model is not permitted.')

class GovFinLedgerAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    list_display = ('acctid', 'submitted', 'name', 'subid', 'amount', 'voidedby')
    list_filter = ('acctid',)
    actions = []

    def get_readonly_fields(self, request, obj=None):
        all_readonly = ['acctid', 'submitted', 'voidedby', 'byuser']
        if obj:
            return all_readonly + ['name', 'subid', 'amount']
        return all_readonly

    def has_add_permission(self, request, obj=None):
        return False

    def get_actions(self, request):
        return []

    def get_list_display_links(self, request, list_display):
        return ['name']

    def has_delete_permission(self, request, obj=None):
        return False

    def save_model(self, request, obj, form, change):
        raise Exception('changes to financial subaccounts are not allowed')

    def get_queryset(self, request):
        return super(GovFinLedgerAdmin, self).get_queryset(request)#.order_by('-submitted')

    def delete_model(self, request, obj):
        raise Exception('delete on this model is not permitted.')


admin.site.register(GovFinAccount, GovFinAccountAdmin)
admin.site.register(GovFinSubaccount, GovFinSubaccountAdmin)
admin.site.register(GovFinLedger, GovFinLedgerAdmin)
