import logging
import os

from django.conf import settings
from django.contrib.gis.geos import GEOSGeometry, Point, LineString, Polygon, MultiPolygon
from django.contrib.gis.geos.error import GEOSException

from datapunt_generic.batch import batch
from datapunt_generic.generic import database

from datapunt_generic.generic.csv import process_csv
from datasets.themas.models import Thema
from . import models

log = logging.getLogger(__name__)


class ImportTask(batch.BasicTask):
    path = None

    def __init__(self):
        diva = settings.DIVA_DIR
        if not os.path.exists(diva):
            raise ValueError("DIVA_DIR not found: {}".format(diva))

        self.path = os.path.join(diva, 'milieuthemas')


class ImportHoogtebeperkendeVlakkenTask(ImportTask):
    name = "Import dro_schiphol_hoogtes"
    themas = set()

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

        except GEOSException as msg:
            log.warn("Geluidzone {} unable to encapsulate GEOS geometry {}; skipping".format(
                    row['id'],
                    msg
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


class ImportGeluidzoneTask(ImportTask):
    name = "Import dro_geluid_schiphol"
    themas = set()

    def before(self):
        database.clear_models(models.Geluidzone)
        self.themas = frozenset(Thema.objects.values_list('id', flat=True))

    def after(self):
        self.themas = None

    def process(self):
        source = os.path.join(self.path, "dro_geluid_schiphol.csv")
        zones = [zone for zone in process_csv(source, self.process_row) if zone]

        models.Geluidzone.objects.bulk_create(zones, batch_size=database.BATCH_SIZE)

    def process_row(self, row):
        thema_id = int(row['tma_id'])

        if thema_id not in self.themas:
            log.warn("Geluidzone {} references non-existing thema {}; skipping".format(row['id'], thema_id))
            return

        geom = None
        try:
            geom = GEOSGeometry(row['geometrie'])
        except GEOSException as msg:
            log.warn("Geluidzone {} unable to encapsulate GEOS geometry {}; skipping".format(
                    row['id'],
                    msg
            ))
            pass

        if isinstance(geom, Polygon):
            geom = MultiPolygon(geom)

        return models.Geluidzone(
            geo_id=int(row['id']),
            type=row['type'],
            thema_id=thema_id,
            geometrie=geom,
        )


class ImportVogelvrijwaringsgebiedTask(ImportTask):
    name = "Import dro_vogel"
    themas = set()

    def before(self):
        database.clear_models(models.Vogelvrijwaringsgebied)
        self.themas = frozenset(Thema.objects.values_list('id', flat=True))

    def after(self):
        self.themas = None

    def process(self):
        source = os.path.join(self.path, "dro_vogel.csv")
        gebieden = [gebied for gebied in process_csv(source, self.process_row) if gebied]

        models.Vogelvrijwaringsgebied.objects.bulk_create(gebieden, batch_size=database.BATCH_SIZE)

    def process_row(self, row):
        thema_id = int(row['tma_id'])

        if thema_id not in self.themas:
            log.warn("Vogelvrijwaringsgebied {} references non-existing thema {}; skipping".format(row['id'], thema_id))
            return

        geom = None
        try:
            geom = GEOSGeometry(row['geometrie'])
        except GEOSException as msg:
            log.warn("Vogelvrijwaringsgebied {} unable to encapsulate GEOS geometry {}; skipping".format(
                    row['id'],
                    msg
            ))
            pass

        if isinstance(geom, Polygon):
            geom = MultiPolygon(geom)

        return models.Vogelvrijwaringsgebied(
            geo_id=int(row['id']),
            type=row['type'],
            thema_id=thema_id,
            geometrie=geom,
        )


class ImportSchipholJob(object):
    name = "Import schiphol"

    def tasks(self):
        return [
            ImportHoogtebeperkendeVlakkenTask(),
            ImportGeluidzoneTask(),
            ImportVogelvrijwaringsgebiedTask()
        ]
