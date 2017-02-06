from django.contrib.sites.models import Site
from django.db import migrations

from geo_views import migrate
from milieuthemas import settings

API_DOMAIN = 'API Domain'


def create_site(apps, *args, **kwargs):
    Site.objects.update_or_create(
        domain=settings.DATAPUNT_API_URL,
        name=API_DOMAIN
    )


def delete_site(apps, *args, **kwargs):
    Site.objects.filter(name='API Domain').delete()


class Migration(migrations.Migration):
    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('sites', '0002_alter_domain_unique'),
        ('bommenkaart', '0004_auto_20170206_1453'),
    ]

    operations = [
        migrate.ManageView(
            view_name='geo_bommenkaart_bominslag_point',
            sql=f"""
                SELECT
                  bominslag.bron,
                  bominslag.oorlogsinc,
                  'bommenkaart/bominslag' as type,
                  bominslag.type as detail_type,
                  bominslag.kenmerk as display,
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
            """),

        migrate.ManageView(
            view_name='geo_bommenkaart_gevrijwaardgebied_polygon',
            sql=f"""
                SELECT
                  gg.bron,
                  'bommenkaart/gevrijwaardgebied' as type,
                  gg.type as detail_type,
                  gg.kenmerk as display,
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
                  'bommenkaart/uitgevoerdonderzoek' as type,
                  uo.type as detail_type,
                  uo.kenmerk as display,
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
                  'bommenkaart/verdachtgebied' as type,
                  vg.type as detail_type,
                  vg.kenmerk as display,
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
