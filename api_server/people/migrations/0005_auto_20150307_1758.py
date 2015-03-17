# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('people', '0004_auto_20150307_1748'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='directory',
            options={'managed': False, 'verbose_name': 'Directory Entry', 'verbose_name_plural': 'Directory Entries'},
        ),
        migrations.AlterModelTable(
            name='directory',
            table='public_active_directory',
        ),
    ]
