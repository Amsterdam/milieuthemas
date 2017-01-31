from django.db import migrations

from geo_views import migrate

API_DOMAIN = 'API Domain'


class Migration(migrations.Migration):
    dependencies = [
        ('geo_views', '0001_add_urls_to_bommenkaart'),
        ('bommenkaart', '0002_add_missing_fields'),
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
                  bominslag.pdf,
                  bominslag.intekening,
                  site.domain || 'milieuthemas/explosieven/inslagen/' || bominslag.id || '/' AS uri,
                  bominslag.geometrie_point AS geometrie
                FROM
                  bommenkaart_bominslag bominslag , django_site site
                WHERE
                  bominslag.geometrie_point IS NOT NULL and site.name = '{API_DOMAIN}';
            """),

        migrate.ManageView(
            view_name='geo_bommenkaart_gevrijwaardgebied_polygon',
            sql=f"""
                SELECT
                  gg.bron,
                  gg.type,
                  gg.kenmerk,
                  gg.opmerkingen,
                  gg.id,
                  gg.nauwkeurig,
                  gg.intekening,
                  gg.datum,
                  site.domain || 'milieuthemas/explosieven/gevrijwaardgebied/' || gg.id || '/' AS uri,
                  gg.geometrie_polygon AS geometrie
                FROM
                  bommenkaart_gevrijwaardgebied gg, django_site site
                WHERE
                  gg.geometrie_polygon IS NOT NULL and site.name = '{API_DOMAIN}';
            """.format(api_domain=API_DOMAIN)),

        migrate.ManageView(
            view_name='geo_bommenkaart_uitgevoerdonderzoek_polygon',
            sql=f"""
                SELECT
                  uo.type,
                  uo.kenmerk,
                  uo.id,
                  uo.opdrachtnemer,
                  uo.verdacht_gebied,
                  uo.onderzoeksgebied,
                  uo.datum,
                  uo.opdrachtgever,
                  site.domain || 'milieuthemas/explosieven/uitgevoerdonderzoek/' || uo.id || '/' AS uri,
                  uo.geometrie_polygon AS geometrie
                FROM
                  bommenkaart_uitgevoerdonderzoek uo, django_site site
                WHERE
                  uo.geometrie_polygon IS NOT NULL and site.name = '{API_DOMAIN}';
            """.format(api_domain=API_DOMAIN)),

        migrate.ManageView(
            view_name='geo_bommenkaart_verdachtgebied_polygon',
            sql=f"""
                SELECT
                  vg.bron,
                  vg.afbakening,
                  vg.aantal,
                  vg.cartografie,
                  vg.type,
                  vg.kenmerk,
                  vg.horizontaal,
                  vg.id,
                  vg.kaliber,
                  vg.subtype,
                  vg.oorlogshandeling,
                  vg.verschijning,
                  vg.pdf,
                  vg.opmerkingen,
                  site.domain || 'milieuthemas/explosieven/verdachtgebied/' || vg.id || '/' AS uri,
                  vg.geometrie_polygon AS geometrie
                FROM
                  bommenkaart_verdachtgebied vg, django_site site
                WHERE
                  vg.geometrie_polygon IS NOT NULL and site.name = '{API_DOMAIN}';
            """.format(api_domain=API_DOMAIN))
    ]