from django.db import models
from django.db.models import CharField

SDB_MODELS = (
    ('people', 'directory'),
    ('people', 'public_active_directory'),
    ('people', 'sds_users_all'),

    ('packages', 'packages'),

    ('api_server', 'sds_users_all'),
)
def check_in_sdb(model):
    return (model._meta.app_label, model._meta.db_table) in SDB_MODELS

class SdbRouter(object): 
    def db_for_read(self, model, **hints):
        if check_in_sdb(model):
            return 'sdb'
        return None

    def db_for_write(self, model, **hints):        
        if check_in_sdb(model):
            #raise Exception('writes not allowed')
            return 'sdb'
        return None
    
    def allow_relation(self, obj1, obj2, **hints):
        "Allow any relation if a both models in chinook app"
        if check_in_sdb(obj1) and check_in_sdb(obj2):
            return True
        elif not check_in_sdb(obj1) and not check_in_sdb(obj2): 
            return True
        return False
    
    def allow_syncdb(self, db, model):
        if db == 'sdb' or check_in_sdb(model):
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
