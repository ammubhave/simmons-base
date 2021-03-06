from django.db import models
from django.contrib.auth.models import User
#from lounges.models import Lounge
from api_server.sdb_utils import NullableCharField
#rom api_server.sdb_utils import SdbManager


class DirectoryManager(models.Manager):
    def get_queryset(self):
        return super(DirectoryManager, self).get_query_set().filter(username__in=[u.username for u in User.objects.all()], active=True)


class Directory(models.Model):
    username = models.CharField(max_length=255, primary_key=True)
    firstname = models.CharField(max_length=255)
    lastname = models.CharField(max_length=255)
    room = NullableCharField(max_length=255, null=True, blank=True)
    year = NullableCharField(max_length=255, null=True, blank=True)
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
    lounge = models.ForeignKey('lounges.Lounge', db_column='lounge', blank=True, null=True)
    title = NullableCharField(max_length=255, null=True, blank=True)
    loungevalue = models.IntegerField(null=True, blank=True)
    showreminders = models.BooleanField(default=True)
    guest_list_expiration = models.CharField(null=True, blank=True, max_length=255)

    #def save(self, *args, **kwargs):
    #    return

    def delete(self, *args, **kwargs):
        raise Exception('You should not be calling delete on this model (directory)')

    @staticmethod
    def random():
        import random as r
        count = Directory.objects.count()
        random_index = r.randint(0, count - 1)
        return Directory.objects.all()[random_index]

    #objects = SdbManager()

    class Meta:
        db_table = 'directory' #'public_active_directory'
        managed = False
        verbose_name = 'Directory Entry'
        verbose_name_plural = 'Directory Entries'

    def __unicode__(self):
        return '%s %s (%s)' % (self.firstname, self.lastname, self.username)


class MedlinkManager(models.Manager):
    def get_queryset(self):
        return super(MedlinkManager, self).get_query_set().filter(removed=None)


class Medlink(models.Model):
    officerid = models.AutoField(primary_key=True)
    #username = models.CharField(max_length=255)
    username = models.ForeignKey(Directory, db_column='username')#, related_name='username')
    ordering = models.IntegerField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    removed = models.DateTimeField(null=True, blank=True)

    objects = MedlinkManager()

    def delete(self, *args, **kwargs):
        raise Exception('You should not be calling delete on this model (medlink)')

    class Meta:
        db_table = 'medlinks'
        managed = False
        verbose_name = 'Medlink'
        verbose_name_plural = 'Medlinks'

    def __unicode__(self):
        return str(self.username)# '%s %s (%s)' % (self.username.firstname, self.username.lastname, self.username)


class OfficerManager(models.Manager):
    def get_queryset(self):
        return super(OfficerManager, self).get_query_set().filter(removed=None)


class Officer(models.Model):
    officerid = models.AutoField(primary_key=True)
    username = models.ForeignKey(Directory, db_column='username')
    position = models.TextField()
    ordering = models.IntegerField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    removed = models.DateTimeField(null=True, blank=True)
    position_text = models.TextField(null=True, blank=True)

    objects = OfficerManager()

    def delete(self, *args, **kwargs):
        raise Exception('You should not be calling delete on this model (officers)')

    class Meta:
        db_table = 'officers'
        managed = False
        verbose_name = 'Officer'
        verbose_name_plural = 'Officers'

    def __unicode__(self):
        return str(self.username) + ' (' + self.position + ') '# '%s %s (%s)' % (self.username.firstname, self.username.lastname, self.username)
