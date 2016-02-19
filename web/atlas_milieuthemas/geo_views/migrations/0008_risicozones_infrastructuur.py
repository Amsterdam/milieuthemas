# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-02-19 15:41
from __future__ import unicode_literals

from django.db import migrations
from geo_views import migrate

class Migration(migrations.Migration):

    dependencies = [
        ('geo_views', '0007_risicozones_bedrijven'),
        ('risicozones_infrastructuur', '0001_initial'),
    ]

    operations = [
        migrate.ManageView(
            view_name="geo_risicozones_infrastructuur_aardgasleidingen",
            sql="""SELECT id, geometrie_line AS geometrie
                    FROM risicozones_infrastructuur_infrastructuur
                    WHERE geometrie_line IS NOT NULL AND type = 'ag'"""
        ),
        migrate.ManageView(
            view_name="geo_risicozones_infrastructuur_spoorwegen",
            sql="""SELECT id, geometrie_polygon AS geometrie
                    FROM risicozones_infrastructuur_infrastructuur
                    WHERE geometrie_polygon IS NOT NULL AND type = 'sw'"""
        ),
        migrate.ManageView(
            view_name="geo_risicozones_infrastructuur_vaarwegen",
            sql="""SELECT id, geometrie_polygon AS geometrie
                    FROM risicozones_infrastructuur_infrastructuur
                    WHERE geometrie_polygon IS NOT NULL AND type = 'vw'"""
        ),
        migrate.ManageView(
            view_name="geo_risicozones_infrastructuur_wegen",
            sql="""SELECT id, geometrie_polygon AS geometrie
                    FROM risicozones_infrastructuur_infrastructuur
                    WHERE geometrie_polygon IS NOT NULL AND type = 'wg'"""
        ),
        
    ]
