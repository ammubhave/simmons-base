from django.db import models
from api_server.sdb_utils import NullableCharField
#from composite_field import CompositeField

class SDB_sds_users_all(models.Model):
    username = models.CharField(max_length=255, primary_key=True)
    password = NullableCharField(max_length=255, null=True, blank=True)
    salt = NullableCharField(max_length=255, null=True, blank=True)
    active = models.BooleanField(default=True)
    hosts_allow = models.CharField(max_length=255, default='%')
    immortal = models.BooleanField(default=False)

    class Meta:
        db_table = 'sds_users_all'
        managed = False

    def __unicode__(self):
        return self.username

class SDB_old_room_assignments(models.Model):
    username = models.ForeignKey(SDB_sds_users_all)
    room = models.CharField(max_length=255) # TODO: Make this a foreign key
    movein = models.DateTimeField(auto_now_add=True)
    moveout = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'old_room_assignments'
        managed = False
        unique_together = []
