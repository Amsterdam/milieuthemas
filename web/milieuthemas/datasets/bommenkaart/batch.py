# Python
import csv
import logging
import os
from contextlib import contextmanager

from dateutil.parser import parse
from django.contrib.gis.geos import GEOSGeometry
from django.contrib.gis.geos import MultiPolygon
from django.contrib.gis.geos import Point

from datapunt_generic.batch import batch
from datapunt_generic.generic import database
from . import models

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


def parse_date(datestring):
    """
    Try to parse the date provided in the dataset
    """
    if not datestring:
        return

    try:
        return parse(datestring.replace('/', '-'))
    except ValueError:
        log.error('Invalid date Error "%s"', datestring)


class ImportProces(batch.BasicTask):
    def before(self):
        pass

    def process(self):
        """
        Processing the CSV
        """
        source = os.path.join(self.path, self.source)

        objects = [_object for _object in process_qgis_csv(
            source, self.process_row) if _object]

        self.model.objects.bulk_create(
            objects, batch_size=database.BATCH_SIZE)

    def pdf_link(self, pdf_name):
        """
        The object store link:

        https://data.amsterdam.nl/bommenkaart/RAP_000000_.pdf
        """
        url = "https://data.amsterdam.nl/bommenkaart/{}"
        return url.format(pdf_name)


class ImportInslagenTask(ImportProces):
    name = "import inslagen"
    model = models.BomInslag
    source = "inslagen.csv"

    def before(self):
        """
        Cleaning up before reimport
        """
        database.clear_models(models.BomInslag)

    def process_row(self, row):
        """
        bron header
        wKT         geometrie
        kenmerk     kenmerk
        datum       datum van inslag
        soort_hand  type
        bron1       foto / document
        datum1      datum brondocument
        intekening  Bron informatie?
        nauwkeurig  .
        opmerkinge  .
        oorlogsinc  oorlogsincident_id
        hyperlink   pdf
        """
        if 'kenmerk' not in row:
            print('No id, skipping')
            return

        geom = GEOSGeometry(row['wkt'])

        if isinstance(geom, Point):
            point = geom
        else:
            raise GEOSGeometry('Unworkable Geos type %s' % geom.geom_type)

        return models.BomInslag(
            kenmerk=row['kenmerk'],
            type='bommenkaart/bominslag',
            detail_type=row['soort_hand'],
            geometrie_point=point,
            bron=row['bron1'],
            intekening=row['intekening'],
            nauwkeurig=row['nauwkeurig'],
            opmerkingen=row['opmerkinge'],
            oorlogsinc=row['oorlogsinc'],
            pdf=self.pdf_link(row['hyperlink']),
            datum_inslag=parse_date(row['datum']),
            datum=parse_date(row['datum1'])
        )


class ImportGevrijwaardTask(ImportProces):
    """
    wkt,        geometrie
    kenmerk     kenmerk
    datum       (Wordt niet geïmporteerd)
    soort_hand, (?)
    bron1       foto / document
    datum1,     Datum rapport
    intekening,
    nauwkeurig, (leeg)
    opmerkinge,
    """

    name = "import gevrijwaard_gebied"
    model = models.GevrijwaardGebied
    source = "gevrijwaard_gebied.csv"

    def before(self):
        """
        Cleaning up before reimport
        """
        database.clear_models(models.GevrijwaardGebied)

    def process_row(self, row):

        geom = GEOSGeometry(row['wkt'])

        poly = None

        if isinstance(geom, MultiPolygon):
            poly = geom
        else:
            raise GEOSGeometry('Unworkable Geos type %s' % geom.geom_type)

        return models.GevrijwaardGebied(
            kenmerk=row['kenmerk'],
            type='bommenkaart/gevrijwaardgebied',
            detail_type=row['soort_hand'],
            geometrie_polygon=poly,
            bron=row['bron1'],
            nauwkeurig=row['nauwkeurig'],
            opmerkingen=row['opmerkinge'],
            intekening=row['intekening'],
            datum=parse_date(row['datum1'])
        )


class ImportVerdachtGebiedTask(ImportProces):
    name = "import verdachte gebieden"
    model = models.VerdachtGebied
    source = "verdachte_gebieden.csv"

    def before(self):
        """
        Cleaning up before reimport
        """
        database.clear_models(models.VerdachtGebied)

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

        if isinstance(geom, MultiPolygon):
            poly = geom
        else:
            log.error('Geo error')
            raise GEOSGeometry('Unworkable Geos type %s' % geom.geom_type)

        return models.VerdachtGebied(

            kenmerk=row['kenmerk'],
            type='bommenkaart/verdachtgebied',
            detail_type=row['hoofdgroep'],
            subtype=row['subsoort'],

            aantal=row['aantallen'],
            kaliber=row['kaliber'],
            verschijning=row['verschijni'],

            oorlogshandeling=row['oorlogshan'],
            afbakening=row['afbakening'],

            horizontaal=row['horizontal'],
            cartografie=row['cartografi'],
            opmerkingen=row['opmerkinge'],
            pdf=self.pdf_link(row['hyperlink']),

            geometrie_polygon=poly,
        )


class ImportUitgevoerdOnderzoekTask(ImportProces):
    name = "import onderzochte gebieden"
    model = models.UitgevoerdOnderzoek
    source = "reeds_uitgevoerd_ce_onderzoek.csv"

    def before(self):
        """
        Cleaning up before reimport
        """
        database.clear_models(models.UitgevoerdOnderzoek)

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

        if isinstance(geom, MultiPolygon):
            poly = geom
        else:
            log.error('Geo error')
            raise GEOSGeometry('Unworkable Geos type %s' % geom.geom_type)

        return models.UitgevoerdOnderzoek(
            kenmerk=row['kenmerk'],
            type='bommenkaart/uitgevoerdonderzoek',
            detail_type=row['soort_rapp'],
            onderzoeksgebied=row['onderzoeks'],
            opdrachtnemer=row['opdrachtne'],
            opdrachtgever=row['opdrachtge'],
            verdacht_gebied=row['verdacht_g'],
            geometrie_polygon=poly,
            datum=parse_date(row['datum'])
        )


class ImportBommenkaartJob(object):
    name = "Import bommenkaart informatie"

    def tasks(self):
        return [
            ImportInslagenTask(path='Bommenkaart/bommenkaart/csv'),
            ImportVerdachtGebiedTask(path='Bommenkaart/bommenkaart/csv/'),
            ImportUitgevoerdOnderzoekTask(path='Bommenkaart/bommenkaart/csv/'),
            ImportGevrijwaardTask(path='Bommenkaart/bommenkaart/csv/'),
        ]
