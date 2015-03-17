# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('sevenk', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='sevenkupload',
            options={'verbose_name': '7K Upload', 'verbose_name_plural': '7K Uploads'},
        ),
        migrations.AlterField(
            model_name='sevenkupload',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, to_field=b'username'),
            preserve_default=True,
        ),
    ]
