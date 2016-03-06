from django.db import models
from django.contrib.auth.models import User
from api_server import sdb_models
from people.models import Directory
from api_server.sdb_utils import NullableCharField
#rom api_server.sdb_utils import SdbManager


class GuestlistManager(models.Manager):
    def get_queryset(self):
        return super(GuestlistManager, self).get_query_set().filter(current=True)


class Guestlist(models.Model):
    guestlistid = models.AutoField(primary_key=True)
    username = models.ForeignKey(Directory, db_column='username')#, related_name='recipient')
    guest = models.TextField(null=False)
    date_added = models.DateTimeField(auto_now_add=True, null=False)
    date_invalid = models.DateTimeField(null=False)
    current = models.BooleanField(default=True)
    onetime = models.BooleanField(default=False)

    objects = GuestlistManager()

    #def save(self, *args, **kwargs):
    #    return

    def delete(self, *args, **kwargs):
        raise Exception('You should not be calling delete on this model (guest_list)')

    class Meta:
        db_table = 'guest_list'
        managed = False
        verbose_name = 'Guest List Entry'
        verbose_name_plural = 'Guest List Entries'

    def __unicode__(self):
        return self.recipient.username
