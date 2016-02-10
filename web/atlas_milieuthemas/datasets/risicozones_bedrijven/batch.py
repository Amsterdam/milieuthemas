import logging
import os

from django.contrib.gis.geos import GEOSGeometry, Point, Polygon, MultiPolygon
from django.contrib.gis.geos.error import GEOSException

from datapunt_generic.batch import batch
from datapunt_generic.generic import database

from datapunt_generic.generic.csv import process_csv, parse_nummer
from . import models

log = logging.getLogger(__name__)


class ImportLPGVulpuntTask(batch.BasicTask):
    name = "Import dmb_lpg_vulpunt"

    def before(self):
        database.clear_models(models.LPGVulpunt)

    def after(self):
        pass

    def process(self):
        source = os.path.join(self.path, "dmb_lpg_vulpunt.csv")
        vulpunten = [vulpunt for vulpunt in process_csv(source, self.process_row) if vulpunt]

        models.LPGVulpunt.objects.bulk_create(vulpunten, batch_size=database.BATCH_SIZE)

    def process_row(self, row):
        if not row['id']:
            return

        point, poly = None, None

        try:
            geom = GEOSGeometry(row['geometrie'])

            if isinstance(geom, Point):
                point = geom

            if isinstance(geom, Polygon):
                poly = MultiPolygon(geom)

            if isinstance(geom, MultiPolygon):
                poly = geom

        except GEOSException as msg:
            log.warn("LPGVulpunt {} unable to encapsulate GEOS geometry {}; skipping".format(
                    row['id'],
                    msg
            ))
            pass

        return models.LPGVulpunt(
            geo_id=int(row['id']),
            stationnummer=parse_nummer(row['stationnummer']),
            type=row['type_contour'],
            afstandseis=row['afstandseis'],
            voldoet=row['voldoet'],
            geometrie_point=point,
            geometrie_polygon=poly,
        )


class ImportLPGAfleverzuilTask(batch.BasicTask):
    name = "Import dmb_lpg_afleverzuil"

    def before(self):
        database.clear_models(models.LPGAfleverzuil)

    def after(self):
        pass

    def process(self):
        source = os.path.join(self.path, "dmb_lpg_afleverzuil.csv")
        zuilen = [zuil for zuil in process_csv(source, self.process_row) if zuil]

        models.LPGAfleverzuil.objects.bulk_create(zuilen, batch_size=database.BATCH_SIZE)

    def process_row(self, row):
        point, poly = None, None

        try:
            geom = GEOSGeometry(row['geometrie'])

            if isinstance(geom, Point):
                point = geom

            if isinstance(geom, Polygon):
                poly = MultiPolygon(geom)

            if isinstance(geom, MultiPolygon):
                poly = geom

        except GEOSException as msg:
            log.warn("LPGAfleverzuil {} unable to encapsulate GEOS geometry {}; skipping".format(
                    row['id'],
                    msg
            ))
            pass

        return models.LPGAfleverzuil(
            stationnummer=parse_nummer(row['stationnummer']),
            geometrie_point=point,
            geometrie_polygon=poly,
        )


class ImportLPGTankTask(batch.BasicTask):
    name = "Import dmb_lpg_tank"

    def before(self):
        database.clear_models(models.LPGTank)

    def after(self):
        pass

    def process(self):
        source = os.path.join(self.path, "dmb_lpg_tank.csv")
        tanks = [tank for tank in process_csv(source, self.process_row) if tank]

        models.LPGTank.objects.bulk_create(tanks, batch_size=database.BATCH_SIZE)

    def process_row(self, row):
        if not row['type_contour']:
            return

        geom = GEOSGeometry(row['geometrie'])

        if isinstance(geom, Polygon):
            geom = MultiPolygon(geom)

        return models.LPGTank(
            stationnummer=parse_nummer(row['stationnummer']),
            kleur=parse_nummer(row['stationnummer'] or 0),
            type=row['type_contour'],
            voldoet=row['voldoet'],
            afstandseis=row['afstandseis'],
            geometrie=geom,
        )


class ImportRisicozonesBedrijvenJob(object):
    name = "Import risicozones bedrijven"

    def tasks(self):
        return [
            ImportLPGVulpuntTask(),
            ImportLPGAfleverzuilTask(),
            ImportLPGTankTask(),
        ]
