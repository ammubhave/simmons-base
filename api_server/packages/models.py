from django.db import models
from django.contrib.auth.models import User
from api_server import sdb_models
from people.models import Directory
from api_server.sdb_utils import NullableCharField
#rom api_server.sdb_utils import SdbManager


class PackageManager(models.Manager):
    def get_queryset(self):
        return super(PackageManager, self).get_query_set().filter(pickup=None)


class Package(models.Model):
    packageid = models.AutoField(primary_key=True)
    recipient = models.ForeignKey(Directory, db_column='recipient')#, related_name='recipient')
    bin = models.CharField(max_length=255)
    checkin = models.DateTimeField(auto_now_add=True)
    checkin_by = models.ForeignKey(Directory, db_column='checkin_by', related_name='recipient_package')#, related_name='checkin_by')
    pickup = models.DateTimeField(null=True, blank=True)
    pickup_by = models.ForeignKey(Directory, null=True, blank=True, db_column='pickup_by', related_name='pickup_by_recipient')
    perishable = models.BooleanField(default=False)

    objects = PackageManager()

    #def save(self, *args, **kwargs):
    #    return

    def delete(self, *args, **kwargs):
        raise Exception('You should not be calling delete on this model (packages)')

    class Meta:
        db_table = 'packages'
        managed = False
        verbose_name = 'Package'
        verbose_name_plural = 'Packages'

    def __unicode__(self):
        return self.recipient.username
