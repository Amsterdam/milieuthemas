# Python
import logging
import os
import csv

from contextlib import contextmanager

# Packages
from django.contrib.gis.geos import GEOSGeometry
from django.contrib.gis.geos import Point
from django.contrib.gis.geos import LineString
from django.contrib.gis.geos import MultiPolygon

from django.contrib.gis.geos.error import GEOSException

# Project
from . import models
from datapunt_generic.batch import batch
from datapunt_generic.generic import database

log = logging.getLogger('bommenkaart')
log.setLevel(logging.DEBUG)


def _wrap_row(r, headers):
    return dict(zip(headers, r))


@contextmanager
def _context_reader(source):
    """
    Read csv line by line yield dict with values
    """

    if not os.path.exists(source):
        raise ValueError("File not found: {}".format(source))

    with open(source) as f:

        rows = csv.reader(f, delimiter=',')
        headers = [h.lower() for h in next(rows)]

        yield (_wrap_row(r, headers) for r in rows)


def process_qgis_csv(source, process_row_callback):
    """
    We load exported qgis files
    """
    with _context_reader(source) as rows:
        return [result for result in (
                process_row_callback(r) for r in rows)
                if result]


class ImportInslagenTask(batch.BasicTask):
    name = "import inslagen"
    model = models.BomInslag

    def before(self):
        """
        Cleaning up before reimport
        """
        database.clear_models(models.BomInslag)

    def after(self):
        """
        No cleanup werk needed
        """
        pass

    def process(self):
        """
        Processing the CSV
        """
        source = os.path.join(self.path, "inslagen.csv")

        inslagen = [inslag for inslag in process_qgis_csv(
            source, self.process_row) if inslag]

        models.BomInslag.objects.bulk_create(
            inslagen, batch_size=database.BATCH_SIZE)

    def process_row(self, row):
        """
        bron header
        wKT         geometrie
        kenmerk     kenmerk
        datum       datum
        soort_hand  type
        bron1       foto / document
        datum1      als datum1 er niet is dan 2 wel
        intekening  Bron informatie?
        nauwkeurig  .
        opmerkinge  .
        oorlogsinc  oorlogsincident_id
        hyperlink   pdf
        """
        if 'kenmerk' not in row:
            print('No id, skipping')
            return

        point = None

        geom = GEOSGeometry(row['wkt'])

        if isinstance(geom, Point):
            point = geom
        else:
            raise GEOSGeometry('Unworkable Geos type %s' % geom.geom_type)

        datum = row['datum']

        if not datum:
            datum = row['datum1']

        m = models.BomInslag(
            kenmerk=row['kenmerk'],
            type=row['soort_hand'],
            # datum=datum,
            geometrie_point=point,
            nauwkeurig=row['nauwkeurig'],
            opmerkingen=row['opmerkinge'],
            oorlogsinc=row['oorlogsinc'],
            pdf=row['hyperlink']  # FIXME create working link..
        )
        # m.save()
        return m

# class ImportGevrijwaardTask(batch.BasicTask):
#    name = "import gevrijwaard_gebied"
#
#    def before(self):
#        """
#        Cleaning up before reimport
#        """
#        # database.clear_models(models.Brisantbom)
#        pass
#
#    def after(self):
#        """
#        No cleanup werk needed
#        """
#        pass
#
#    def process(self):
#        """
#        Processing the CSV
#        """
#        return
#        source = os.path.join(self.path, "inslagen.csv")
#        brisantbommen = [brisantbom for brisantbom in process_csv(source, self.process_row) if brisantbom]
#        models.Brisant.bulk_create(bristabommen, batch_size=database.BATCH_SIZE)
#        log.info(models.GevrijwaardGebied.objects.count())
#
#    def process_row(self, row):
#
#
# class ImportOnderzochtTask(batch.BasicTask):
#     name = "import reeds_uitgevoerd_ce_onderzoeken"
#
#     def before(self):
#         """
#         Cleaning up before reimport
#         """
#         # database.clear_models(models.Brisantbom)
#         pass
#
#     def after(self):
#         """
#         No cleanup werk needed
#         """
#         pass
#
#     def process(self):
#         """
#         Processing the CSV
#         """
#         return
#         source = os.path.join(self.path, "reeds_uitgevoerd_ce_onderzoek.csv")
#         brisantbommen = [brisantbom for brisantbom in process_csv(source, self.process_row) if brisantbom]
#
#         models.Brisant.bulk_create(bristabommen, batch_size=database.BATCH_SIZE)
#         log.info(models.OnderzochtGebied.objects.count())
#
#     def process_row(self, row):
#         return None
#
#
#
# class ImportVerdachtTask(batch.BasicTask):
#     name = "import verdacht gebied"
#
#     def before(self):
#         """
#         Cleaning up before reimport
#         """
#         return
#         #database.clear_models(models.Brisantbom)
#
#     def after(self):
#         """
#         No cleanup werk needed
#         """
#         pass
#
#     def process(self):
#         """
#         Processing the CSV
#         """
#         return
#
#         source = os.path.join(self.path, "gevrijwaard_gebied.csv")
#         brisantbommen = [brisantbom for brisantbom in process_csv(source, self.process_row) if brisantbom]
#
#         models.Brisant.bulk_create(bristabommen, batch_size=database.BATCH_SIZE)
#
#     def process_row(self, row):
#

class ImportBommenkaartJob(object):
    name = "Import bommenkaart informatie"

    def tasks(self):
        return[
            ImportInslagenTask(path='bommenkaart/csv'),

            # ImportVerdachtTask(path='bommenkaart/csv/'),
            # ImportOnderzochtTask(path='bommenkaart/csv/'),
            # ImportGevrijwaardTask(path='bommenkaart/csv/'),
        ]
