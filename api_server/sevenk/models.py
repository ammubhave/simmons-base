from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class SevenKUpload(models.Model):
    user = models.ForeignKey(User, to_field='username', db_column='user')
    uploaded = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    class Meta:              
        verbose_name = '7K Upload'
        verbose_name_plural = '7K Uploads'

    def __unicode__(self):
        return self.user.username + ' - ' + self.name  
