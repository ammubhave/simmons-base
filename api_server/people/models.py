from django.db import models

# Create your models here.
class Directory(models.Model):
    username = models.TextField(primary_key=True)
    firstname = models.TextField()
    lastname = models.TextField()
    room = models.TextField(null=True, blank=True)
    year = models.IntegerField(null=True, blank=True)
    title = models.TextField(null=True, blank=True)
    private = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        return

    def delete(self, *args, **kwargs):
        return

    class Meta:
        db_table = 'public_active_directory'
        managed = False
