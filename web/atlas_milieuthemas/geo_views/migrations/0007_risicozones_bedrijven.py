# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-02-17 08:15
# Python
from __future__ import unicode_literals
# Packages
from django.db import migrations
# Project
from geo_views import migrate


class Migration(migrations.Migration):

    dependencies = [
        ('geo_views', '0006_veiligheidsafstanden'),
        ('risicozones_bedrijven', '0009_auto_20160218_1425'),
    ]

    operations = [
        migrate.ManageView(
            view_name="geo_risicozones_bedrijven_lpgstation_point_layer",
            sql="""SELECT id, bedrijfsnaam, dossiernummer,
                    geometrie_point AS geometrie
                    FROM risicozones_bedrijven_lpgstation
                    WHERE geometrie_point IS NOT NULL"""
        ),
        migrate.ManageView(
            view_name="geo_risicozones_bedrijven_lpgstation_polygon_layer",
            sql="""SELECT id, bedrijfsnaam, dossiernummer,
                    geometrie_polygon AS geometrie
                    FROM risicozones_bedrijven_lpgstation
                    WHERE geometrie_polygon IS NOT NULL"""
        ),
        migrate.ManageView(
            view_name="geo_risicozones_bedrijven_lpgvulpunt_point_layer",
            sql="""SELECT id, type, afstandseis, voldoet,
                    geometrie_point AS geometrie
                    FROM risicozones_bedrijven_lpgvulpunt
                    WHERE geometrie_point IS NOT NULL"""
        ),
        migrate.ManageView(
            view_name="geo_risicozones_bedrijven_lpgvulpunt_polygon_layer",
            sql="""SELECT id, type, afstandseis, voldoet,
                    geometrie_polygon AS geometrie
                    FROM risicozones_bedrijven_lpgvulpunt
                    WHERE geometrie_polygon IS NOT NULL"""
        ),
        migrate.ManageView(
            view_name="geo_risicozones_bedrijven_lpgtank",
            sql="""SELECT id, type, afstandseis, voldoet, geometrie
                    FROM risicozones_bedrijven_lpgtank
                    WHERE geometrie IS NOT NULL"""
        ),
        migrate.ManageView(
            view_name="geo_risicozones_bedrijven_lpgafleverzuil_point_layer",
            sql="""SELECT id, station_id, geometrie_point AS geometrie
                    FROM risicozones_bedrijven_lpgafleverzuil
                    WHERE geometrie_point IS NOT NULL"""
        ),
        migrate.ManageView(
            view_name="geo_risicozones_bedrijven_lpgafleverzuil_polygon_layer",
            sql="""SELECT id, station_id, geometrie_polygon AS geometrie
                    FROM risicozones_bedrijven_lpgafleverzuil
                    WHERE geometrie_polygon IS NOT NULL"""
        ),

    ]
