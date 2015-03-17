from django.contrib import admin
from models import Package
from people.models import Directory
#from api_server.sdb_models import SDB_sds_users_all
#from django.utils.http import quote
from django import forms
#from urllib import quote

class PackageModelAdminForm(forms.ModelForm):
    pass
    # def clean_username(self):
    #     username = self.cleaned_data['username']
    #     if self.instance.pk is None or self.instance.pk == '':
    #         if SDB_sds_users_all.objects.filter(username=username).exists():
    #             raise forms.ValidationError(username + ' is already in the DB. Are you sure this user is not disabled?')
    #     return username

def action_checkin_packages(modeladmin, request, queryset):
    from datetime import datetime
    queryset.update(pickup_by=Directory.objects.get(username=request.user.username), pickup=datetime.now())
action_checkin_packages.short_description = 'Mark selected Packages as picked up'

class PackageModelAdmin(admin.ModelAdmin):
    form = PackageModelAdminForm
    list_filter = ('bin','perishable') # lounge foriegn field
    search_fields = ('recipient__username', 'recipient__firstname', 'recipient__lastname')
    list_display = ('recipient','bin','checkin','checkin_by','perishable')
    #list_editable = ('bin','perishable')
    actions = [action_checkin_packages]
    # fieldsets = (
    #     (None, {
    #         'fields': ('username', 'title', 'firstname', 'lastname', 'room', 'year', 'email', 'type', 'private')
    #     }),
    #     ('Directory Information', {
    #         'classes': ('collapse',),
    #         'fields': ('homepage', 'cellphone', 'home_city', 'home_state', 'home_country', 'quote', 'favorite_category', 'favorite_value')
    #     })
    # )
    raw_id_fields = ('recipient','checkin_by')
    # def view_on_site(self, obj):
    #     return 'https://seagull.mit.edu/sds/directory/entry.php?username=' + quote(str(obj.username))


    #def has_add_permission(self, request, obj=None):
    #    return False

    # actions = [] # TODO: Add bulk download as CSV button

    def get_actions(self, request):
        actions = super(PackageModelAdmin, self).get_actions(request)
        if 'delete_selected' in actions:
                del actions['delete_selected']
        return actions

    def get_fields(self, request, obj=None):
        fields = ['recipient', 'bin', 'perishable']
        if False: # request.user.is_superuser:
            return fields + ['checkin', 'checkin_by']
        return fields

    def get_readonly_fields(self, request, obj=None):
        all_readonly = ['checkin', 'checkin_by']
        #if True:# not request.user.is_superuser:
        if obj:
            return all_readonly + ['recipient']
        return all_readonly

    def get_list_display_links(self, request, list_display):
        return None

   # def get_form(self, request, obj=None, **kwargs):
   #    form = super(PackageModelAdmin, self).get_form(request, obj, **kwargs)
        #import pprint
        #raise Exception(pprint.pformat(form.hidden_fields(form)))
        #raise Exception(str(dir(form)))
        #form.base_fields['checkin_by'].initial = request.user.username
        #return form

    #def has_delete_permission(self, request, obj=None):
    #    return False

    def save_model(self, request, obj, form, change):
        if not change:
            from datetime import datetime
            obj.checkin_by = Directory.objects.get(username=request.user.username)
            obj.checkin = datetime.now()
        obj.save()
        #raise Exception('title:' + str(form.cleaned_data['title']))
        #raise Exception(str(form.changed_data))

        # if change:
        #     pass # this is save
        # else:
        #     # this is an insert
        #     SDB_sds_users_all.objects.create(username=form.cleaned_data['username'], active=True, immortal=False)
        #     if (form.cleaned_data['room'] is not None and form.cleaned_data['room'] != ''):
        #         SDB_old_room_assignments.objects.create(username=form.cleaned_data['username'], room=form.cleaned_data['room'])
        pass
        #raise Exception('save on this model is not permitted.')

    #def get_queryset(self, request):
    #    return super(DirectoryModelAdmin, self).get_queryset(request).using(self.using).filter(private=False, username__in=)

    def delete_model(self, request, obj):
        raise Exception('delete on this model is not permitted.')

admin.site.register(Package, PackageModelAdmin)
