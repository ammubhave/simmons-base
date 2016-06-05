from django.contrib import admin
#from models import SevenKUpload

# class SevenKUploadModelAdmin(admin.ModelAdmin):
#     search_fields = ('user','name','description',)
#     list_display = ('user', 'name',)
#     raw_id_fields = ('user',)
#     def view_on_site(self, obj):
#     	return 'javascript: alert("Not Implemented");'
#         #return 'https://seagull.mit.edu/sds/directory/entry.php?username=' + quote(str(obj.username))

#     #def save_model(self, request, obj, form, change):
#         #if not change:
#         #    from datetime import datetime
#         #    obj.checkin_by = Directory.objects.get(username=request.user.username)
#         #    obj.checkin = datetime.now()
#         # TODO: Save 7K Upload
#         # obj.save()
#         #raise Exception('title:' + str(form.cleaned_data['title']))
#         #raise Exception(str(form.changed_data))

#         # if change:
#         #     pass # this is save
#         # else:
#         #     # this is an insert
#         #     SDB_sds_users_all.objects.create(username=form.cleaned_data['username'], active=True, immortal=False)
#         #     if (form.cleaned_data['room'] is not None and form.cleaned_data['room'] != ''):
#         #         SDB_old_room_assignments.objects.create(username=form.cleaned_data['username'], room=form.cleaned_data['room'])
#         #pass
#         #raise Exception('save on this model is not permitted.')

# # Register your models here.
# admin.site.register(SevenKUpload, SevenKUploadModelAdmin)
