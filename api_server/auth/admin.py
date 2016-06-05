from django.contrib import admin
from models import SdbUser, SdbGroup
from auth.models import SDB_sds_group_membership_cache
from django import forms
from django.contrib.admin.widgets import FilteredSelectMultiple

class SdbUserChangeForm(forms.ModelForm):
    groups = forms.ModelMultipleChoiceField(
       queryset=SdbGroup.objects.all(),
       widget=FilteredSelectMultiple('SdbGroup', False))

    def __init__(self, *args, **kwargs):
        if 'instance' in kwargs:
            initial = kwargs.setdefault('initial', {})
            initial['groups'] = [t.groupname.pk for t in kwargs['instance'].groups_set.all()]

        super(SdbUserChangeForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        if not self.is_valid():
            raise HttpResponseForbidden
        instance = super(SdbUserChangeForm, self).save(self, commit)
        def save_m2m_with_through():
            groups = [t for t in self.cleaned_data['groups']]
            old_groups = instance.groups_set.all()
            for old in old_groups:
                if old.groupname not in groups:
                    old.delete()
            for group in [x for x in groups not in map(lambda x: x.groupname, old_groups)]:                   
                membership = SDB_sds_group_membership_cache(groupname=group, username=instance)
                membership.save()
        if commit:
            save_m2m_with_through()
        else:
            self.save_m2m = save_m2m_with_through
        return instance

    class Meta:
        model = SdbUser
        fields = '__all__'

class SdbUserModelAdmin(admin.ModelAdmin):
    list_display = ('username', 'is_staff', 'is_superuser')
    list_filter =  ('is_active',)#('is_staff', 'is_superuser', 'is_active')#, 'groups')
    search_fields = ('username',)
    ordering = ('username',)
    fieldsets = (
        (None, {'fields': ('username', 'password','salt')}),
        ('Permissions', {'fields': ('is_active','groups',)}),
    )
    form = SdbUserChangeForm
    #filter_horizontal = ('groups',)#, 'user_permissions',)

    def has_add_permission(self, request, obj=None):
        return False

    def get_readonly_fields(self, request, obj=None):
        return []

    def has_delete_permission(self, request, obj=None):
        return False

    def save_model(self, request, obj, form, change):
        raise Exception('save on this model is not permitted.')

    def delete_model(self, request, obj):
        raise Exception('delete on this model is not permitted.')

admin.site.register(SdbUser, SdbUserModelAdmin)


class SdbGroupModelAdmin(admin.ModelAdmin):
    list_display = ('groupname', 'contact', 'active')
    list_filter =  ('active',)#('is_staff', 'is_superuser', 'is_active')#, 'groups')
    search_fields = ('groupname',)
    ordering = ('groupname','active')
    #filter_horizontal = ('groups')#, 'user_permissions',)

    def has_add_permission(self, request, obj=None):
        return False

    def get_readonly_fields(self, request, obj=None):
        return []

    def has_delete_permission(self, request, obj=None):
        return False

    def save_model(self, request, obj, form, change):
        raise Exception('save on this model is not permitted.')

    def delete_model(self, request, obj):
        raise Exception('delete on this model is not permitted.')

admin.site.register(SdbGroup, SdbGroupModelAdmin)
