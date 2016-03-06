from django.db import models
from people.models import Directory

# Create your models here.

class Lounge(models.Model):
    lounge = models.CharField(max_length=255, primary_key=True)
    description = models.TextField()
    url = models.TextField()
    contact = models.ForeignKey(Directory, db_column='contact')
    contact2 = models.ForeignKey(Directory, db_column='contact2', null=True, blank=True)
    active = models.BooleanField(default=True)
    allocation = models.DecimalField(max_digits=10, decimal_places=2)

    def to_dict(self):
        return {
            'lounge': self.lounge,
            'description': self.description,
        }

    def delete(self, *args, **kwargs):
        raise Exception('You should not be calling delete on this model (lounge)')

    class Meta:
        db_table = 'lounges'
        managed = False
        verbose_name = 'Lounge'
        verbose_name_plural = 'Lounges'

    def __unicode__(self):
        return '%s (%s)' % (self.description, self.lounge)
