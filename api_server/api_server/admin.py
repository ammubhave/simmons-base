from django.contrib import admin
from sdb_models import SDB_sds_users_all

class SdbReadonlyModelAdmin(admin.ModelAdmin):
    using = 'sdb'

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        if request.method not in ('GET', 'HEAD'):
            return False
        return super(SdbReadonlyModelAdmin, self).has_change_permission(request, obj) 

    def get_readonly_fields(self, request, obj=None):
        return self.fields or [f.name for f in self.model._meta.fields] 

    def has_delete_permission(self, request, obj=None):
        return False

    def save_model(self, request, obj, form, change):
        raise Exception('save on this model is not permitted.')

    def delete_model(self, request, obj):
        raise Exception('delete on this model is not permitted.')

    #def get_queryset(self, request):
    #    return super(SdbReadonlyModelAdmin, self).get_queryset(request).using(self.using)


# class SDB_sds_users_all_ModelAdmin(SdbReadonlyModelAdmin):
#     search_fields = ('username', 'firstname', 'lastname')
#     list_display = ('username','firstname','lastname', 'title', 'room', 'year')

#     def get_queryset(self, request):
#         return super(SDB_sds_users_all_ModelAdmin, self).get_queryset(request)

# admin.site.register(SDB_sds_users_all, SDB_sds_users_all_ModelAdmin)
