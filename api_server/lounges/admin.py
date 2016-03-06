from django.contrib import admin
from models import Lounge
# Register your models here.
class LoungeModelAdmin(admin.ModelAdmin):
    list_filter = ('active',)
    list_display = ('description','lounge','active','contact','contact2')

admin.site.register(Lounge, LoungeModelAdmin)