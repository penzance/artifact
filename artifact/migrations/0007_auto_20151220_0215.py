# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('artifact', '0006_map_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='map',
            name='description',
            field=models.CharField(max_length=500),
        ),
        migrations.AlterField(
            model_name='markers',
            name='external_url',
            field=models.CharField(default=b'', max_length=250),
        ),
    ]
