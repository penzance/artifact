# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('artifact', '0002_auto_20151001_1950'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='map',
            name='context_id',
        ),
        migrations.RemoveField(
            model_name='map',
            name='resource_link_id',
        ),
    ]
