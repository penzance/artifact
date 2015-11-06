# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('artifact', '0003_auto_20151002_1407'),
    ]

    operations = [
        migrations.AddField(
            model_name='markers',
            name='file',
            field=models.FileField(upload_to=b'', blank=True),
        ),
    ]
