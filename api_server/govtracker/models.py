from django.db import models
from people.models import Directory


class GovFinAccount(models.Model):
    acctid = models.AutoField(primary_key=True)
    name = models.TextField()
    shortname = models.TextField()

    class Meta:
        db_table = 'gov_fin_accounts'
        managed = False
        verbose_name = 'Gov Financial Account'
        verbose_name_plural = 'Gov Financial Accounts'

    def __unicode__(self):
        return self.name

class GovFinSubaccount(models.Model):
    subid = models.AutoField(primary_key=True)
    acctid = models.ForeignKey(GovFinAccount, db_column='acctid', verbose_name='Account')
    name = models.TextField()
    created = models.DateTimeField(auto_now_add=True, verbose_name='Created On')
    allocationamt = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Allocation Amount')
    isallocation = models.BooleanField(default=True, verbose_name='Is Allocation')
    shortname = models.TextField()
    byuser = models.ForeignKey(Directory, db_column='byuser', verbose_name='Created By', related_name='subaccount')
    closedby = models.ForeignKey(Directory, db_column='closedby', null=True, blank=True, verbose_name='Closed By')
    closedat = models.DateTimeField(null=True, blank=True, verbose_name='Closed At')

    class Meta:
        db_table = 'gov_fin_subaccounts'
        managed = False
        verbose_name = 'Gov Financial Subaccount'
        verbose_name_plural = 'Gov Financial Subaccounts'

    def __unicode__(self):
        return self.name

class GovFinLedger(models.Model):
    tid = models.AutoField(primary_key=True)
    subid = models.ForeignKey(GovFinSubaccount, db_column='subid', verbose_name='Subaccount')
    name = models.TextField()
    submitted = models.DateTimeField(auto_now_add=True)
    byuser = models.ForeignKey(Directory, db_column='byuser', verbose_name='Created By', related_name='ledger')
    acctid = models.ForeignKey(GovFinAccount, db_column='acctid', verbose_name='Account')
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Amount')
    voidedby = models.ForeignKey(Directory, db_column='voidedby', verbose_name='Voided By', null=True, blank=True)

    class Meta:
        db_table = 'gov_fin_ledger'
        managed = False
        verbose_name = 'Gov Financial Ledger'
        verbose_name_plural = 'Gov Financial Ledger'

    def __unicode__(self):
        return self.name
