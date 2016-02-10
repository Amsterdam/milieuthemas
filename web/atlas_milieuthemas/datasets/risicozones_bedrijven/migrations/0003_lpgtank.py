# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-02-10 11:59
from __future__ import unicode_literals

import django.contrib.gis.db.models.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('risicozones_bedrijven', '0002_lpgafleverzuil'),
    ]

    operations = [
        migrations.CreateModel(
            name='LPGTank',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('stationnummer', models.IntegerField(null=True)),
                ('kleur', models.IntegerField(null=True)),
                ('type', models.CharField(max_length=40, null=True)),
                ('voldoet', models.CharField(max_length=3, null=True)),
                ('afstandseis', models.CharField(max_length=10, null=True)),
                ('geometrie', django.contrib.gis.db.models.fields.MultiPolygonField(null=True, srid=28992)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
