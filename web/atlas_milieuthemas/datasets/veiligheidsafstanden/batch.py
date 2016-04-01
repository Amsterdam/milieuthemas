import logging
import os

from django.contrib.gis.geos import GEOSGeometry, Polygon, MultiPolygon, Point
from django.contrib.gis.geos.error import GEOSException

from datapunt_generic.batch import batch
from datapunt_generic.generic import database

from datapunt_generic.generic.csv import process_csv
from datasets.themas.models import Thema
from . import models

log = logging.getLogger(__name__)


class ImportVeiligheidsafstandenTask(batch.BasicTask):
    name = "Import dro_veiligheid"
    themas = set()

    def before(self):
        database.clear_models(models.Veiligheidsafstand)
        self.themas = frozenset(Thema.objects.values_list('id', flat=True))

    def after(self):
        self.themas = None

    def process(self):
        source = os.path.join(self.path, "dro_veiligheid.csv")
        afstanden = [afstand for afstand in process_csv(source, self.process_row) if afstand]

        models.Veiligheidsafstand.objects.bulk_create(afstanden, batch_size=database.BATCH_SIZE)

    def process_row(self, row):
        thema_id = int(row['tma_id'])

        if thema_id not in self.themas:
            log.warn("Veiligheidsafstand {} references non-existing thema {}; skipping".format(row['id'], thema_id))
            return

        geom_point, geom_poly = None, None

        geom = None
        try:
            geom = GEOSGeometry(row['geometrie'])
        except GEOSException as msg:
            log.warn("Veiligheidsafstand {} unable to encapsulate GEOS geometry {}; skipping".format(
                    row['id'],
                    msg
            ))
            pass

        if isinstance(geom, Point):
            geom_point = geom

        if isinstance(geom, Polygon):
            geom_poly = MultiPolygon(geom)

        return models.Veiligheidsafstand(
            geo_id=int(row['id']),
            type=row['type'],
            thema_id=thema_id,
            locatie=row['locatie'],
            geometrie_multipolygon=geom_poly,
            geometrie_point=geom_point,
        )


class ImportVeiligheidsafstandenJob(object):
    name = "Import veiligheid"

    def tasks(self):
        return [
            ImportVeiligheidsafstandenTask(),
        ]
