# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations

from geo_views import migrate


class Migration(migrations.Migration):
    dependencies = [
        ('schiphol', '0001_initial')
    ]

    operations = [
        migrate.ManageView(
            view_name="geo_schiphol_hoogte_point_layer",
            sql=""
                "SELECT id, geo_id, type, geometrie_point as geometrie "
                "FROM schiphol_hoogtebeperkendevlakken "
                "WHERE geometrie_point IS NOT NULL"
        ),
        migrate.ManageView(
            view_name="geo_schiphol_hoogte_line_layer",
            sql="SELECT id, geo_id, type, geometrie_line as geometrie "
                "FROM schiphol_hoogtebeperkendevlakken "
                "WHERE geometrie_line IS NOT NULL"
        ),
        migrate.ManageView(
            view_name="geo_schiphol_hoogte_polygon_layer",
            sql="SELECT id, geo_id, type, geometrie_polygon as geometrie "
                "FROM schiphol_hoogtebeperkendevlakken "
                "WHERE geometrie_polygon IS NOT NULL"
        ),
    ]
