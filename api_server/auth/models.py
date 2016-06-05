from django.db import models
from django.contrib.auth.models import BaseUserManager
from api_server.sdb_models import NullableCharField, SDB_sds_group_membership_cache
from people.models import Directory


# class SdbGroupMembershipCache(models.Model):
#     username = models.ForeignKey('SdbUser', primary_key=True, db_column='username', related_name='username')
#     groupname = models.ForeignKey('SdbGroup', db_column='groupname', related_name='groupname')
#     hosts_allow = models.CharField(max_length=255)

#     class Meta:
#         db_table = 'sds_group_membership_cache'
#         managed = False
#         unique_together = (("username", "groupname"))

#     def __unicode__(self):
#         return self.username + ' - ' + self.groupname


class SdbGroup(models.Model):
    groupname = models.CharField(max_length=255, primary_key=True)
    contact = models.CharField(max_length=255)
    adhoc = models.BooleanField(default=False, null=False)
    description = models.TextField()
    active = models.BooleanField(default=True, null=False)

    class Meta:
        db_table = 'sds_groups'
        managed = False
        verbose_name = 'group'
        verbose_name_plural = 'groups'

    def __unicode__(self):
        return self.groupname


class SdbUserManager(BaseUserManager):
    def create_user(self, username):
        raise Exception('Creation of user not permitted')

    def create_superuser(self, username):
        raise Exception('Creation of superuser not permitted')

# Create your models here.
class SdbUser(models.Model):
    username = models.CharField(max_length=255, primary_key=True)
    password = NullableCharField(max_length=255, null=True, blank=True)
    salt = NullableCharField(max_length=255, null=True, blank=True)
    is_active = models.BooleanField(default=True, db_column='active')
    hosts_allow = models.CharField(max_length=255, default='%')
    immortal = models.BooleanField(default=False)

    groups = models.ManyToManyField(
        SdbGroup,
        verbose_name='Groups',
        blank=True,
        through=SDB_sds_group_membership_cache,
        through_fields=('username','groupname'),
        related_name='users_set',
    )

    objects = SdbUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    class Meta:
        db_table = 'sds_users_all'
        managed = False
        verbose_name = 'user'
        verbose_name_plural = 'users'

    def get_username(self):
        "Return the identifying username for this User"
        return getattr(self, self.USERNAME_FIELD)

    def save(self, *args, **kwargs):
        return
        # super(AbstractBaseUser, self).save(*args, **kwargs)
        # if self._password is not None:
        #     password_validation.password_changed(self._password, self)
        #     self._password = None

    def natural_key(self):
        return (self.get_username(),)

    def is_anonymous(self):
        return False

    def is_authenticated(self):
        return True

    def get_full_name(self):
        e = Directory.objects.filter(username=self.username)
        if len(e) > 0:
            e = e[0]
            return e.firstname + ' ' + e.lastname
        else:
            return '<NO NAME>'

    def get_short_name(self):
        e = Directory.objects.filter(username=self.username)
        if len(e) > 0:
            e = e[0]
            return e.firstname
        else:
            return '<NO NAME>'

    @property
    def is_staff(self):
        return self.is_superuser

    @property
    def is_superuser(self):
        e = SDB_sds_group_membership_cache.objects.filter(username=self.username, groupname='ADMINISTRATORS')
        return len(e) != 0

    def has_perm(self, perm, obj=None):
        if self.is_active and self.is_superuser:
            return True
        return False
        e = SDB_sds_group_membership_cache.objects.filter(username=self.username, groupname=perm)
        return len(e) != 0

    def has_perms(self, perms, obj=None):
        if self.is_active and self.is_superuser:
            return True
        return False

    def has_model_perms(self, app_label):
        return True

    def has_module_perms(self, module_name):
        return True

    def get_group_permissions(obj=None):
        return []

    def get_all_permissions(obj=None):
        return []

    def __unicode__(self):
        return self.username
