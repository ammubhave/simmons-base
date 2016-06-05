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

class SDB_sds_groups(models.Model):
    groupname = models.CharField(max_length=255, primary_key=True)
    contact = models.CharField(max_length=255)
    adhoc = models.BooleanField(default=False, null=False)
    description = models.TextField()
    active = models.BooleanField(default=True, null=False)

    class Meta:
        db_table = 'sds_groups'
        managed = False

    def __unicode__(self):
        return self.groupname

class SDB_sds_group_membership_cache(models.Model):
    #username = models.ForeignKey(SDB_sds_users_all, primary_key=True, db_column='username', related_name='username')
    #groupname = models.ForeignKey(SDB_sds_groups, db_column='groupname', related_name='groupname')
    username = models.ForeignKey('auth.SdbUser', primary_key=True, db_column='username', related_name='groups_set')
    groupname = models.ForeignKey('auth.SdbGroup', db_column='groupname', related_name='users_set')
    hosts_allow = models.CharField(max_length=255)

    class Meta:
        db_table = 'sds_group_membership_cache'
        managed = False
        unique_together = (("username", "groupname"))

    def __unicode__(self):
        return self.username + ' - ' + self.groupname
