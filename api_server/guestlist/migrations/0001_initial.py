# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Package',
            fields=[
                ('packageid', models.AutoField(serialize=False, primary_key=True)),
                ('bin', models.CharField(max_length=255)),
                ('checkin', models.DateTimeField(auto_now_add=True)),
                ('pickup', models.DateTimeField(null=True, blank=True)),
                ('perishable', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'Package',
                'db_table': 'packages',
                'managed': False,
                'verbose_name_plural': 'Packages',
            },
            bases=(models.Model,),
        ),
    ]
