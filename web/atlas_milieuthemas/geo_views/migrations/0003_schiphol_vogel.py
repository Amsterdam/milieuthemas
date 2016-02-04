# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations

from geo_views import migrate


class Migration(migrations.Migration):
    dependencies = [
        ('schiphol', '0004_vogelvrijwaringsgebied'),
        ('geo_views', '0002_schiphol_geluid')
    ]

    operations = [
        migrate.ManageView(
            view_name="geo_schiphol_vogelvrijwaringsgebied",
            sql="SELECT id, geo_id, type, geometrie "
                "FROM schiphol_vogelvrijwaringsgebied "
                "WHERE geometrie IS NOT NULL"
        ),
    ]
