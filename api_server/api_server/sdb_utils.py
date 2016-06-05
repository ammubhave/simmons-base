from django.db import models
from django.db.models import CharField

# SDB_MODELS = (
#     ('people', 'directory'),
#     ('people', 'public_active_directory'),
#     ('people', 'sds_users_all'),

#     ('packages', 'packages'),

#     ('api_server', 'sds_users_all'),
# )

DB_MAP = {
    ('lounges', 'lounges'): 'sdb',
    ('people', 'directory'): 'sdb',
    ('people', 'public_active_directory'): 'sdb',
    ('people', 'sds_users_all'): 'sdb',
    ('people', 'medlinks'): 'sdb',
    ('people', 'officers'): 'sdb',
    ('packages', 'packages'): 'sdb',
    ('guestlist', 'guest_list'): 'sdb',
    ('api_server', 'sds_users_all'): 'sdb',
    ('api_server', 'sds_groups'): 'sdb',
    ('api_server', 'sds_group_membership_cache'): 'sdb',
    ('auth', 'sds_users_all'): 'sdb',
    ('auth', 'sds_groups'): 'sdb',
    ('admin', 'django_admin_log'): 'sdb',
    ('govtracker', 'gov_fin_accounts'): 'sdb',
    ('govtracker', 'gov_fin_subaccounts'): 'sdb',
    ('govtracker', 'gov_fin_ledger'): 'sdb',

    ('rooming', 'rooming_room'): 'scripts_rooming',
    ('rooming', 'rooming_grt'): 'scripts_rooming',
    ('rooming', 'rooming_resident'): 'scripts_rooming',
}

READONLY_TABLES = (
    ('api_server', 'sds_groups'),
    ('api_server', 'sds_users_all'),
    ('auth', 'sds_users_all'),
    #('api_server', 'sds_group_membership_cache'),
)

def check_in_db_map(model):
    return (model._meta.app_label, model._meta.db_table) in DB_MAP

#def check_in_sdb(model):
#    return (model._meta.app_label, model._meta.db_table) in SDB_MODELS

class SdbRouter(object):
    def db_for_read(self, model, **hints):
        #if model._meta.app_label == 'oauth2_provider':
        #    raise Exception(model._meta.db_table)
        if check_in_db_map(model):
            return DB_MAP[(model._meta.app_label, model._meta.db_table)] #'sdb'
        return 'default'

    def db_for_write(self, model, **hints):
        #if model._meta.app_label == 'oauth2_provider':
        #    raise Exception(model._meta.db_table)
        if check_in_db_map(model):
            #raise Exception('writes not allowed')
            if (model._meta.app_label, model._meta.db_table) in READONLY_TABLES:
                raise Exception('writes not allowed to a readonly table')
            return DB_MAP[(model._meta.app_label, model._meta.db_table)]
        return 'default'

    def allow_relation(self, obj1, obj2, **hints):
        "Allow any relation if a both models in chinook app"
        if check_in_db_map(obj1) and check_in_db_map(obj2) and DB_MAP[(obj1._meta.app_label, obj1._meta.db_table)] == DB_MAP[(obj2._meta.app_label, obj2._meta.db_table)]:
            return True
        elif not check_in_db_map(obj1) and not check_in_db_map(obj2):
            return True
        return False

    def allow_syncdb(self, db, model):
        if db == 'sdb' or db == 'scripts_rooming' or check_in_db_map(model):
            return False
        else:
            return True

class SdbManager(models.Manager):
    def get_queryset(self):
        return super(SdbManager, self).get_query_set().using('sdb')
        # qs = super(MultiDBManager, self).get_query_set()
        # qs.query.connection = self.get_db_wrapper()
        # return qs

class NullableCharField(CharField):
    def get_db_prep_value(self, value, *args, **kwargs):
        if self.blank == self.null == True and value == '':
            value = None
        return super(NullableCharField, self).get_db_prep_value(value, *args, **kwargs)
