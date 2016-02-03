import logging
import os

from django.contrib.gis.geos import GEOSGeometry, Point, LineString, Polygon, MultiPolygon
from django.contrib.gis.geos.error import GEOSException

from datapunt_generic.batch import batch
from datapunt_generic.generic import database

from datapunt_generic.generic.csv import process_csv
from datasets.themas.models import Thema
from . import models

log = logging.getLogger(__name__)


class ImportHoogtebeperkendeVlakkenTask(batch.BasicTask):
    name = "Import dro_schiphol_hoogtes"
    themas = set()

    def __init__(self, path):
        self.path = path

    def before(self):
        database.clear_models(models.HoogtebeperkendeVlakken)
        self.themas = frozenset(Thema.objects.values_list('id', flat=True))

    def after(self):
        self.themas = None

    def process(self):
        source = os.path.join(self.path, "dro_schiphol_hoogtes.csv")
        vlakken = [vlak for vlak in process_csv(source, self.process_row) if vlak]

        models.HoogtebeperkendeVlakken.objects.bulk_create(vlakken, batch_size=database.BATCH_SIZE)

    def process_row(self, row):
        thema_id = int(row['tma_id'])

        if thema_id not in self.themas:
            log.warn("Hoogtebeperkend vlak {} references non-existing thema {}; skipping".format(row['id'], thema_id))
            return

        point, line, poly = None, None, None

        try:
            geom = GEOSGeometry(row['geometrie'])

            if isinstance(geom, Point):
                point = geom

            if isinstance(geom, LineString):
                line = geom

            if isinstance(geom, Polygon):
                poly = MultiPolygon(geom)

            if isinstance(geom, MultiPolygon):
                poly = geom

        except GEOSException:
            log.warn("Hoogtebeperkend vlak {} unable to encapsulate GEOS geometry {}; skipping".format(
                    row['geo_id'],
                    row['geometrie']
            ))
            pass

        return models.HoogtebeperkendeVlakken(
            geo_id=int(row['id']),
            type=row['type'],
            thema_id=thema_id,
            bouwhoogte=row['bouwhoogte'],
            helling=row['helling'],
            geometrie_point=point,
            geometrie_line=line,
            geometrie_polygon=poly,
        )
