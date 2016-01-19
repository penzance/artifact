# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('artifact', '0005_remove_markers_file'),
    ]

    operations = [
        migrations.AddField(
            model_name='map',
            name='description',
            field=models.CharField(default=b'description', max_length=500),
        ),
    ]
