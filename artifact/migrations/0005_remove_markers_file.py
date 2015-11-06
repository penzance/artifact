# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('artifact', '0004_markers_file'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='markers',
            name='file',
        ),
    ]
