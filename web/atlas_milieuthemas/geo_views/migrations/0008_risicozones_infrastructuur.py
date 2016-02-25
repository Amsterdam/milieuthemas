# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-02-19 15:41
from __future__ import unicode_literals

from django.db import migrations
from geo_views import migrate

class Migration(migrations.Migration):

    dependencies = [
        ('geo_views', '0007_risicozones_bedrijven'),
        ('risicozones_infrastructuur', '0003_auto_20160225_0735'),
    ]

    operations = [
       operations = [
           migrate.ManageView(
               view_name="geo_risicozones_infrastructuur_aardgasgebied_100let",
               sql="""SELECT id, geometrie
                       FROM risicozones_infrastructuur_aardgasgebied
                       WHERE geometrie IS NOT NULL AND type='la'"""
           ),
           migrate.ManageView(
               view_name="geo_risicozones_infrastructuur_aardgasgebied_1let",
               sql="""SELECT id, geometrie
                       FROM risicozones_infrastructuur_aardgasgebied
                       WHERE geometrie IS NOT NULL AND type='l1'"""
           ),
           migrate.ManageView(
               view_name="geo_risicozones_infrastructuur_aardgasgebied_zakelijk",
               sql="""SELECT id, geometrie
                       FROM risicozones_infrastructuur_aardgasgebied
                       WHERE geometrie IS NOT NULL AND type='zk'"""
           ),
           migrate.ManageView(
               view_name="geo_risicozones_infrastructuur_aardgasgebied_plaatsgebonden_risico",
               sql="""SELECT id, geometrie
                       FROM risicozones_infrastructuur_aardgasgebied
                       WHERE geometrie IS NOT NULL AND type='pr'"""
           ),
           migrate.ManageView(
               view_name="geo_risicozones_infrastructuur_aardgasleidingen",
               sql="""SELECT id, geometrie
                       FROM risicozones_infrastructuur_aardgasleiding
                       WHERE geometrie IS NOT NULL"""
           ),
           migrate.ManageView(
               view_name="geo_risicozones_infrastructuur_spoorwegen",
               sql="""SELECT id, geometrie
                       FROM risicozones_infrastructuur_infrastructuur
                       WHERE geometrie IS NOT NULL AND type = 'sw'"""
           ),
           migrate.ManageView(
               view_name="geo_risicozones_infrastructuur_vaarwegen",
               sql="""SELECT id, geometrie
                       FROM risicozones_infrastructuur_infrastructuur
                       WHERE geometrie IS NOT NULL AND type = 'vw'"""
           ),
           migrate.ManageView(
               view_name="geo_risicozones_infrastructuur_wegen",
               sql="""SELECT id, geometrie
                       FROM risicozones_infrastructuur_infrastructuur
                       WHERE geometrie IS NOT NULL AND type = 'wg'"""
           ),
    ]
