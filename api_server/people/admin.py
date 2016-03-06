from django.contrib import admin
from models import Directory, Medlink
from api_server.sdb_models import SDB_sds_users_all
from django.utils.http import quote
from django import forms
from django.db import connections
#from urllib import quote

class DirectoryModelAdminForm(forms.ModelForm):
    def clean_username(self):
        username = self.cleaned_data['username']
        if self.instance.pk is None or self.instance.pk == '':
            if SDB_sds_users_all.objects.filter(username=username).exists():
                raise forms.ValidationError(username + ' is already in the DB. Are you sure this user is not disabled?')
        return username


class DirectoryModelAdmin(admin.ModelAdmin):
    form = DirectoryModelAdminForm
    list_filter = ('type','year') # lounge foriegn field
    search_fields = ('username','title','firstname','lastname','home_city','home_state','home_country')
    list_display = ('username','title','firstname', 'lastname','year','room','email','type','lounge')
    list_editable = ('title','room')
    fieldsets = (
        (None, {
            'fields': ('username', 'title', 'firstname', 'lastname', 'room', 'year', 'email', 'type', 'private')
        }),
        ('Directory Information', {
            'classes': ('collapse',),
            'fields': ('lounge','homepage', 'cellphone', 'home_city', 'home_state', 'home_country', 'quote', 'favorite_category', 'favorite_value')
        })
    )
    # raw_id_fields = ('',)
    def view_on_site(self, obj):
        return 'https://seagull.mit.edu/sds/directory/entry.php?username=' + quote(str(obj.username))


    #def has_add_permission(self, request, obj=None):
    #    return False

    # actions = [] # TODO: Add bulk download as CSV button


    def get_readonly_fields(self, request, obj=None):
        all_readonly = ['homepage','cellphone','home_city','home_state','home_country','quote','favorite_category','favorite_value']
        if obj:
            return all_readonly + ['username']
        return all_readonly

    #def has_delete_permission(self, request, obj=None):
    #    return False

    def save_model(self, request, obj, form, change):
        #raise Exception('title:' + str(form.cleaned_data['title']))
        #raise Exception(str(form.changed_data))

        if change:
            old_obj = Directory.objects.get(username=obj.username)
            #raise Exception(str(old_obj.room) +  " + " + str(form.cleaned_data['room']))
            if old_obj.room != form.cleaned_data['room']:
                cursor = connections['sdb'].cursor()
                if old_obj.room is not None and old_obj.room != '':
                    cursor.execute("UPDATE old_room_assignments SET moveout = now() WHERE username = %s AND room = %s", (obj.username, old_obj.room))
                if form.cleaned_data['room'] is not None and form.cleaned_data['room'] != '':
                    cursor.execute('INSERT INTO old_room_assignments (username, room) VALUES (%s, %s)', (obj.username, form.cleaned_data['room']))
        else:
            # this is an insert
            SDB_sds_users_all.objects.create(username=form.cleaned_data['username'], active=True, immortal=False)
            if (form.cleaned_data['room'] is not None and form.cleaned_data['room'] != ''):
                cursor = connections['sdb'].cursor()
                cursor.execute('INSERT INTO old_room_assignments (username, room) VALUES (%s, %s)', (form.cleaned_data['username'], form.cleaned_data['room']))
                #SDB_old_room_assignments.objects.create(username=form.cleaned_data['username'], room=form.cleaned_data['room'])
        return super(DirectoryModelAdmin, self).save_model(request, obj, form, change)

        #raise Exception('save on this model is not permitted.')

    def delete_model(self, request, obj):
        raise Exception('delete on this model is not permitted.')

admin.site.register(Directory, DirectoryModelAdmin)


class MedlinkModelAdmin(admin.ModelAdmin):
    search_fields = ('username__username', 'username__firstname', 'username__lastname')
    raw_id_fields = ('username')
    # def view_on_site(self, obj):
    #     return 'https://seagull.mit.edu/sds/directory/entry.php?username=' + quote(str(obj.username))
    
    def has_delete_permission(self, request, obj=None):
        return False

    def delete_model(self, request, obj):
        raise Exception('delete on this model is not permitted.')

admin.site.register(Medlink, MedlinkModelAdmin)