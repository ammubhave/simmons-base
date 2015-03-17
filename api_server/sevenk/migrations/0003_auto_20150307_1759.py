# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('sevenk', '0002_auto_20150307_1758'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sevenkupload',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, db_column=b'user', to_field=b'username'),
            preserve_default=True,
        ),
    ]
