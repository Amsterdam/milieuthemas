# -*- coding: utf-8 -*-
# Generated by Django 1.9.10 on 2016-12-01 16:47
from __future__ import unicode_literals

import datapunt_generic.generic.mixins
import django.contrib.gis.db.models.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BomInslag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('kenmerk', models.CharField(max_length=32)),
                ('type', models.CharField(max_length=100, null=True)),
                ('bron', models.CharField(max_length=100, null=True)),
                ('nauwkeurig', models.CharField(max_length=100, null=True)),
                ('datum', models.DateField(null=True)),
                ('opmerkingen', models.TextField(null=True)),
                ('oorlogsinc', models.CharField(max_length=200)),
                ('pdf', models.CharField(max_length=200)),
                ('geometrie_point', django.contrib.gis.db.models.fields.PointField(null=True, srid=28992)),
            ],
            options={
                'abstract': False,
            },
            bases=(datapunt_generic.generic.mixins.ModelViewFieldsMixin, models.Model),
        ),
    ]
