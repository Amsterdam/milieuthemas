from django.db import migrations

from geo_views import migrate

API_DOMAIN = 'API Domain'


class Migration(migrations.Migration):
    dependencies = [
        ('geo_views', '0002_add_missing_fields'),
        ('bommenkaart', '0003_fix_dates'),
    ]

    operations = [
        migrate.ManageView(
            view_name='geo_bommenkaart_bominslag_point',
            sql=f"""
                SELECT
                  bominslag.bron,
                  bominslag.oorlogsinc,
                  bominslag.type,
                  bominslag.kenmerk,
                  bominslag.opmerkingen,
                  bominslag.id,
                  bominslag.nauwkeurig,
                  bominslag.datum,
                  bominslag.datum_inslag,
                  bominslag.pdf,
                  bominslag.intekening,
                  site.domain || 'milieuthemas/explosieven/inslagen/' || bominslag.id || '/' AS uri,
                  bominslag.geometrie_point AS geometrie
                FROM
                  bommenkaart_bominslag bominslag , django_site site
                WHERE
                  bominslag.geometrie_point IS NOT NULL and site.name = '{API_DOMAIN}';
            """)
    ]
