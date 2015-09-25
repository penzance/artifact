# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Map',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('canvas_course_id', models.IntegerField()),
                ('title', models.CharField(max_length=250)),
                ('latitude', models.CharField(max_length=32)),
                ('longitude', models.CharField(max_length=32)),
                ('zoom', models.IntegerField()),
                ('maptype', models.IntegerField(default=2, choices=[(1, b'SATELLITE'), (2, b'ROADMAP'), (3, b'HYBRID'), (4, b'TERRAIN')])),
                ('created_by', models.CharField(max_length=32)),
                ('modified_by', models.CharField(max_length=32)),
                ('date_created', models.DateTimeField(default=django.utils.timezone.now, blank=True)),
                ('date_modified', models.DateTimeField(default=django.utils.timezone.now, blank=True)),
            ],
            options={
                'db_table': 'mp_maps',
            },
        ),
        migrations.CreateModel(
            name='Markers',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=250)),
                ('latitude', models.CharField(max_length=32)),
                ('longitude', models.CharField(max_length=32)),
                ('description', models.CharField(max_length=2000)),
                ('external_url', models.CharField(max_length=250)),
                ('created_by', models.CharField(max_length=32)),
                ('modified_by', models.CharField(max_length=32)),
                ('date_created', models.DateTimeField(default=django.utils.timezone.now, blank=True)),
                ('date_modified', models.DateTimeField(default=django.utils.timezone.now, blank=True)),
                ('map', models.ForeignKey(related_name='markers', to='artifact.Map')),
            ],
            options={
                'db_table': 'mp_markers',
            },
        ),
    ]
