# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('artifact', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='map',
            name='context_id',
            field=models.CharField(default=b'', max_length=50),
        ),
        migrations.AddField(
            model_name='map',
            name='resource_link_id',
            field=models.CharField(default=b'', max_length=50),
        ),
    ]
