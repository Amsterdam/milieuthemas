import csv
import logging
import os

from django.contrib.gis.geos import GEOSGeometry, Polygon, MultiPolygon
from django.contrib.gis.geos.error import GEOSException

from datapunt_generic.batch import batch
from datapunt_generic.generic import database

from datapunt_generic.generic.csv import process_csv
from datasets.themas.models import Thema
from . import models

log = logging.getLogger(__name__)


class ImportMaatgevendeToetshoogteTask(batch.BasicTask):
    name = "Import dro_schiphol_maatgevende_toetshoogte"

    def before(self):
        database.clear_models(models.MaatgevendeToetshoogte)

    def process(self):
        source = os.path.join(self.path, "dro_schiphol_maatgevende_toetshoogte.csv")
        # Note that I'm not using process_csv because my data uses COMMA as
        # separator, not PIPE
        with open(source, newline='') as csvfile:
            data = csv.reader(csvfile)
            models.MaatgevendeToetshoogte.objects.bulk_create(
                self.model_generator(data), batch_size=database.BATCH_SIZE)

    def model_generator(self, data):
        """ Generator that yields an instance of models.MaatgevendeToetshoogte
        for every row in the given data.

        :param data: generator (must implement the iterator protocol). Expects:
            data[n][0] => WKT
            data[n][1] => VLAKNAAM (not used)
            data[n][2] => HOOGTEKLAS
            data[n][3] => H_M_NAP
        """
        _ = next(data)  # headers
        idx_wkt, idx_hoogteklas, idx_h_m_nap = 0, 2, 3
        for row in data:
            try:
                geometrie_polygon = GEOSGeometry(row[idx_wkt])
            except GEOSException as e:
                log.warn('Cannot parse geometry: {}'.format(e))
                continue
            hoogte_nap_klasse = row[idx_hoogteklas]
            hoogte_nap = row[idx_h_m_nap]
            yield models.MaatgevendeToetshoogte(
                geometrie_polygon=geometrie_polygon,
                hoogte_nap_klasse=hoogte_nap_klasse,
                hoogte_nap=hoogte_nap
            )


class ImportHoogtebeperkingRadarTask(batch.BasicTask):
    name = "Import dro_schiphol_radar"

    def before(self):
        database.clear_models(models.HoogtebeperkingRadar)

    def process(self):
        source = os.path.join(self.path, "dro_schiphol_radar.csv")
        # Note that I'm not using process_csv because my data uses COMMA as
        # separator, not PIPE
        with open(source, newline='') as csvfile:
            data = csv.reader(csvfile)
            models.HoogtebeperkingRadar.objects.bulk_create(
                self.model_generator(data), batch_size=database.BATCH_SIZE
            )

    def model_generator(self, data):
        """ Generator that yields an instance of models.HoogtebeperkingRadar
        for every row in the given data.

        :param data: generator (must implement the iterator protocol). Expects:
            data[n][0] => WKT
            data[n][1] => VLAKNAAM (not used)
            data[n][2] => HOOGTEKLAS
            data[n][3] => H_M_NAP
        """
        _ = next(data)  # headers
        idx_wkt, idx_hoogteklas, idx_h_m_nap = 0, 2, 3
        for row in data:
            try:
                geometrie_polygon = GEOSGeometry(row[idx_wkt])
            except GEOSException as e:
                log.warn('Cannot parse geometry: {}'.format(e))
                continue
            hoogte_nap_klasse = row[idx_hoogteklas]
            hoogte_nap = row[idx_h_m_nap]
            yield models.HoogtebeperkingRadar(
                geometrie_polygon=geometrie_polygon,
                hoogte_nap_klasse=hoogte_nap_klasse,
                hoogte_nap=hoogte_nap
            )


class ImportGeluidzoneTask(batch.BasicTask):
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


class ImportVogelvrijwaringsgebiedTask(batch.BasicTask):
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
            ImportMaatgevendeToetshoogteTask(),
            ImportHoogtebeperkingRadarTask(),
            ImportGeluidzoneTask(),
            ImportVogelvrijwaringsgebiedTask()
        ]
