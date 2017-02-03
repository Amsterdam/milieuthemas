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
        ('sites', '0002_alter_domain_unique'),
    ]

    operations = [
        migrations.RunPython(code=create_site, reverse_code=delete_site),

        migrate.ManageView(
            view_name='geo_bommenkaart_bominslag_point',
            sql=f"""
                SELECT
                  bominslag.bron as bron,
                  bominslag.oorlogsinc as oorlogsinc,
                  'bommenkaart/bominslag' as type ,
                  bominslag.kenmerk as display,
                  bominslag.opmerkingen as opmerkingen,
                  bominslag.id as id,
                  bominslag.nauwkeurig as nauwkeurig,
                  bominslag.datum as datum,
                  bominslag.pdf as pdf,
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
                  gg.bron as bron,
                  'bommenkaart/gevrijwaardgebied' as type,
                  gg.kenmerk as display,
                  gg.opmerkingen as opmerkingen,
                  gg.id as id,
                  gg.nauwkeurig as nauwkeurig,
                  gg.datum as datum,
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
                  uo.kenmerk as display,
                  uo.id as id,
                  uo.opdrachtnemer as opdrachtnemer,
                  uo.verdacht_gebied as verdacht_gebied,
                  uo.onderzoeksgebied as onderzoeksgebied,
                  uo.datum as datum,
                  uo.opdrachtgever as opdrachtgever,
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
                  vg.bron as bron,
                  vg.afbakening as afbakening,
                  vg.aantal as aantal,
                  vg.cartografie as cartografie,
                  'bommenkaart/verdachtgebied' as type,
                  vg.kenmerk as display,
                  vg.horizontaal as horizontaal,
                  vg.id as id,
                  vg.kaliber as kaliber,
                  vg.subtype as subtype,
                  vg.oorlogshandeling as oorlogshandeling,
                  vg.verschijning as verschijning,
                  vg.pdf as pdf,
                  site.domain || 'milieuthemas/explosieven/verdachtgebied/' || vg.id || '/' AS uri,
                  vg.geometrie_polygon AS geometrie
                FROM
                  bommenkaart_verdachtgebied vg, django_site site
                WHERE
                  vg.geometrie_polygon IS NOT NULL and site.name = '{API_DOMAIN}';
            """.format(api_domain=API_DOMAIN))
    ]
