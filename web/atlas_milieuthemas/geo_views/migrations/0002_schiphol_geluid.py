# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations

from geo_views import migrate


class Migration(migrations.Migration):
    dependencies = [
        ('schiphol', '0003_geluidzone'),
        ('geo_views', '0001_schiphol_views')
    ]

    operations = [
        migrate.ManageView(
            view_name="geo_schiphol_geluidzone",
            sql="SELECT id, geo_id, type, geometrie as geometrie "
                "FROM schiphol_geluidzone "
                "WHERE geometrie IS NOT NULL"
        ),
    ]
