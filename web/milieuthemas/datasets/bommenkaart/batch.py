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
            datum=datum.replace('/', '-'),
            geometrie_point=point,
            bron=row['bron1'],
            nauwkeurig=row['nauwkeurig'],
            opmerkingen=row['opmerkinge'],
            oorlogsinc=row['oorlogsinc'],
            pdf=row['hyperlink']  # FIXME create working link..
        )

        return m


class ImportGevrijwaardTask(batch.BasicTask):
    """
    wkt,        geometrie
    kenmerk     kenmerk
    datum       datum
    soort_hand, (?)
    bron1       foto / document
    Datum1,
    Intekening,
    Nauwkeurig, (leeg)
    Opmerkinge,
    """

    name = "import gevrijwaard_gebied"
    model = models.GevrijwaardGebied

    def before(self):
        """
        Cleaning up before reimport
        """
        database.clear_models(models.GevrijwaardGebied)

    def process(self):
        """
        Processing the CSV
        """
        source = os.path.join(self.path, "gevrijwaard_gebied.csv")

        gebieden = [
                gebied for gebied in
                process_qgis_csv(source, self.process_row)
                if gebied]

        models.GevrijwaardGebied.objects.bulk_create(
            gebieden, batch_size=database.BATCH_SIZE)

    def process_row(self, row):

        geom = GEOSGeometry(row['wkt'])

        poly = None

        if isinstance(geom, MultiPolygon):
            poly = geom
        else:
            raise GEOSGeometry('Unworkable Geos type %s' % geom.geom_type)

        datum = row['datum']

        if not datum:
            datum = row['datum1']

        m = models.GevrijwaardGebied(
            kenmerk=row['kenmerk'],
            type=row['soort_hand'],
            datum=datum.replace('/', '-'),
            geometrie_polygon=poly,
            bron=row['bron1'],
            nauwkeurig=row['nauwkeurig'],
            opmerkingen=row['opmerkinge'],
        )

        return m


class ImportVerdachtGebiedTask(batch.BasicTask):
    name = "import verdachte gebieden"
    model = models.VerdachtGebied

    def before(self):
        """
        Cleaning up before reimport
        """
        database.clear_models(models.VerdachtGebied)

    def process(self):
        """
        Processing the CSV
        """
        source = os.path.join(self.path, "verdachte_gebieden.csv")

        gebieden = [
                gebied for gebied in
                process_qgis_csv(source, self.process_row)
                if gebied]

        models.VerdachtGebied.objects.bulk_create(
            gebieden, batch_size=database.BATCH_SIZE)

    def process_row(self, row):
        """
        wkt
        kenmerk
        hoofdgroep
        subsoort
        kaliber
        aantallen
        verschijni
        oorlogshan
        afbakening
        horizontal
        cartografi
        opmerkinge
        hyperlink
        """

        geom = GEOSGeometry(row['wkt'])

        poly = None

        if isinstance(geom, MultiPolygon):
            poly = geom
        else:
            log.error('Geo error')
            raise GEOSGeometry('Unworkable Geos type %s' % geom.geom_type)

        m = models.VerdachtGebied(

            kenmerk=row['kenmerk'],

            type=row['hoofdgroep'],
            subtype=row['hoofdgroep'],

            aantal=row['aantallen'],
            kaliber=row['kaliber'],
            verschijning=row['verschijni'],

            oorlogshandeling=row['oorlogshan'],
            afbakening=row['afbakening'],

            horizontaal=row['horizontal'],
            cartografie=row['cartografi'],
            pdf=row['hyperlink'],

            geometrie_polygon=poly,
        )

        return m


class ImportUitgevoerdOnderzoekTask(batch.BasicTask):
    name = "import onderzochte gebieden"
    model = models.UitgevoerdOnderzoek

    def before(self):
        """
        Cleaning up before reimport
        """
        database.clear_models(models.UitgevoerdOnderzoek)

    def process(self):
        """
        Processing the CSV
        """
        source = os.path.join(
            self.path, "reeds_uitgevoerd_ce_onderzoek.csv")

        gebieden = [
                gebied for gebied in
                process_qgis_csv(source, self.process_row)
                if gebied]

        models.UitgevoerdOnderzoek.objects.bulk_create(
            gebieden, batch_size=database.BATCH_SIZE)

    def process_row(self, row):
        """
        wkT
        kenmerk
        soort_rapp
        onderzoeks (gebieds naam)
        opdrachtne
        opdrachtge
        verdacht_g
        datum
        """

        geom = GEOSGeometry(row['wkt'])

        poly = None

        if isinstance(geom, MultiPolygon):
            poly = geom
        else:
            log.error('Geo error')
            raise GEOSGeometry('Unworkable Geos type %s' % geom.geom_type)

        datum = row['datum']

        m = models.UitgevoerdOnderzoek(

            kenmerk=row['kenmerk'],

            type=row['soort_rapp'],

            onderzoeksgebied=row['onderzoeks'],

            opdrachtnemer=row['opdrachtne'],
            opdrachtgever=row['opdrachtge'],

            verdacht_gebied=row['verdacht_g'],

            datum=datum.replace('/', '-'),
            geometrie_polygon=poly,
        )

        return m


class ImportBommenkaartJob(object):
    name = "Import bommenkaart informatie"

    def tasks(self):
        return[
            ImportInslagenTask(path='bommenkaart/csv'),
            ImportVerdachtGebiedTask(path='bommenkaart/csv/'),
            ImportUitgevoerdOnderzoekTask(path='bommenkaart/csv/'),
            ImportGevrijwaardTask(path='bommenkaart/csv/'),
        ]
