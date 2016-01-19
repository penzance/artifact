# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('artifact', '0007_auto_20151220_0215'),
    ]

    operations = [
        migrations.RenameField(
            model_name='map',
            old_name='created_by',
            new_name='created_by_id',
        ),
        migrations.RenameField(
            model_name='map',
            old_name='modified_by',
            new_name='modified_by_id',
        ),
        migrations.RenameField(
            model_name='markers',
            old_name='created_by',
            new_name='created_by_id',
        ),
        migrations.RenameField(
            model_name='markers',
            old_name='modified_by',
            new_name='modified_by_id',
        ),
        migrations.AddField(
            model_name='map',
            name='created_by_full_name',
            field=models.CharField(default='James Curtin', max_length=32),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='markers',
            name='created_by_full_name',
            field=models.CharField(default='James Curtin', max_length=32),
            preserve_default=False,
        ),
    ]
