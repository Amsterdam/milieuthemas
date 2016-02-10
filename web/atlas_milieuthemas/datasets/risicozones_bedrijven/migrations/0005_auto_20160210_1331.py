# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-02-10 13:31
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('risicozones_bedrijven', '0004_lpgstation'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='lpgvulpunt',
            name='stationnummer',
        ),
        migrations.AddField(
            model_name='lpgvulpunt',
            name='station',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='risicozones_bedrijven.LPGStation'),
        ),
    ]
