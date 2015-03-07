from django.db import models
from django.contrib.auth.models import User
from api_server.sdb_utils import NullableCharField
#rom api_server.sdb_utils import SdbManager


class DirectoryManager(models.Manager):
    def get_query_set(self):
        return super(DirectoryManager, self).get_query_set().filter(username__in=[u.username for u in User.objects.all()])


class Directory(models.Model):
    username = models.CharField(max_length=255, primary_key=True)
    firstname = models.CharField(max_length=255)
    lastname = models.CharField(max_length=255)
    room = NullableCharField(max_length=255, null=True, blank=True)
    year = NullableCharField(null=True, blank=True)
    cellphone = models.CharField(max_length=255, null=True, blank=True)
    homepage = models.CharField(max_length=255, null=True, blank=True)
    home_city = models.CharField(max_length=255, null=True, blank=True)
    home_state = models.CharField(max_length=255, null=True, blank=True)
    home_country = models.CharField(max_length=255, null=True, blank=True)
    quote = models.TextField(null=True, blank=True)
    favorite_category = models.CharField(max_length=255, null=True, blank=True)
    favorite_value = models.CharField(max_length=255, null=True, blank=True)
    private = models.BooleanField(default=False)

    ASSOCIATE_HOUSEMASTER = 'AHM'
    GRT = 'GRT'
    HOUSEMASTER = 'HM'
    HOUSE_MANAGER = 'MGR'
    OTHER = 'OTHER'
    RLA = 'RLA'
    UNDERGRADUATE = 'U'
    VISITING_SCHOLAR = 'VS'
    TYPE_CHOICES = (
        (ASSOCIATE_HOUSEMASTER, 'Associate Housemaster'),
        (GRT, 'GRT'),
        (HOUSEMASTER, 'Housemaster'),
        (HOUSE_MANAGER, 'House Manager'),
        (RLA, 'RLA'),
        (UNDERGRADUATE, 'Undergraduate'),
        (VISITING_SCHOLAR, 'Visiting Scholar'),
    )
    type = models.CharField(max_length=255, choices=TYPE_CHOICES)

    email = models.CharField(max_length=255)
    # lounge = models.ForeignField()
    title = NullableCharField(max_length=255, null=True, blank=True)
    # loungevalue = models.IntegerField(null=True, blank=True)
    # showreminders = models.BooleanField(default=True)
    # guest_list_expiration = models.CharField(null=True, blank=True, max_length=255)

    #def save(self, *args, **kwargs):
    #    return

    def delete(self, *args, **kwargs):
        raise Exception('You should not be calling delete on this model (directory)')

    #objects = SdbManager()

    class Meta:
        db_table = 'public_active_directory'
        managed = False
        verbose_name = 'Directory Entry'
        verbose_name_plural = 'Directory Entries'

    def __unicode__(self):
        return self.username
