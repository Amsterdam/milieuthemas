# Python
import csv
import logging
import os
from contextlib import contextmanager

from dateutil.parser import parse
from django.conf import settings
from django.contrib.gis.gdal import DataSource
from django.contrib.gis.geos import GEOSGeometry, Polygon
from django.contrib.gis.geos import MultiPolygon
from django.contrib.gis.geos import Point

from datapunt_generic.batch import batch
from datapunt_generic.generic import database
from . import models

log = logging.getLogger('bommenkaart')
log.setLevel(logging.DEBUG)


def _wrap_row(r, headers):
    return dict(zip(headers, r))


INSLAGEN_PATH = 'Inslagen_ea.shp'
VERDACHTE_GEBIEDEN_PATH = 'Verdachte_gebieden.shp'
UITGEVOERD_ONDERZOEK_PATH = 'Reeds_uitgevoerde_CE_onderzoeken.shp'
GEVRIJWAARD_GEBIED_PATH = 'Gevrijwaard_gebied.shp'

#  TODO : Use new data from shapefiles also for tests
TEST_INSLAGEN_PATH = 'bommenkaart/csv/inslagen.csv'
TEST_VERDACHTE_GEBIEDEN_PATH = 'bommenkaart/csv/verdachte_gebieden.csv'
TEST_UITGEVOERD_ONDERZOEK_PATH = 'bommenkaart/csv/reeds_uitgevoerd_ce_onderzoek.csv'
TEST_GEVRIJWAARD_GEBIED_PATH = 'bommenkaart/csv/gevrijwaard_gebied.csv'


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


def process_shp(source, callback):
    """
    Processes a shape file

    :param source: complete path of file
    :param callback: function taking a shapefile record; called for every row
    :return:
    """
    ds = DataSource(source, encoding='ISO-8859-1')
    lyr = ds[0]

    return [result for result in (callback(feature) for feature in lyr) if result]


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
        Processing the CSV or SHP
        """
        ext = os.path.splitext(self.path)[1]
        if ext == '.csv':
            objects = [_object for _object in process_qgis_csv(
                self.path, self.process_row) if _object]
        elif ext == '.shp':
            objects = [_object for _object in process_shp(
                self.path, self.process_feature) if _object]
        else:
            objects = []

        self.model.objects.bulk_create(
            objects, batch_size=database.BATCH_SIZE)

    def pdf_link(self, pdf_name):
        """
        The object store link:

        https://files.data.amsterdam.nl/bommenkaart/RAP_000000_.pdf
        """
        return f"{settings.FILE_URL_DOMAIN}{settings.FILE_URL_PATH}/{pdf_name}"


class ImportInslagenTask(ImportProces):
    name = "import inslagen"
    model = models.BomInslag

    def before(self):
        """
        Cleaning up before reimport
        """
        database.clear_models(models.BomInslag)

    def process_feature(self, feat):
        geom = GEOSGeometry(feat.geom.wkt)
        if isinstance(geom, Point):
            point = geom
        else:
            raise GEOSGeometry('Unworkable Geos type %s' % geom.geom_type)

        kenmerk = feat.get('Kenmerk')
        if not kenmerk:
            print('No id, skipping')
            return

        return models.BomInslag(
             kenmerk=kenmerk,
             type='bommenkaart/bominslag',
             detail_type=feat['soort_hand'],
             geometrie_point=point,
             bron=feat.get('Bron1'),
             intekening=feat.get('Intekening'),
             nauwkeurig=feat.get('Nauwkeurig'),
             opmerkingen=feat.get('Opmerkinge'),
             oorlogsinc=feat.get('Oorlogsinc'),
             pdf=self.pdf_link(feat.get('Hyperlink')),
             datum_inslag=feat.get('Datum'),
             datum=feat.get('Datum1'),
         )

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

    def before(self):
        """
        Cleaning up before reimport
        """
        database.clear_models(models.GevrijwaardGebied)

    def process_feature(self, feat):
        geom = GEOSGeometry(feat.geom.wkt)
        if isinstance(geom, MultiPolygon):
            poly = geom
        elif isinstance(geom, Polygon):
            poly = MultiPolygon(geom)
        else:
            raise GEOSGeometry('Unworkable Geos type %s' % geom.geom_type)

        kenmerk = feat.get('Kenmerk')
        if not kenmerk:
            print('No id, skipping')
            return

        return models.GevrijwaardGebied(
            kenmerk=feat.get('Kenmerk'),
            type='bommenkaart/gevrijwaardgebied',
            detail_type=feat.get('Soort_hand'),
            geometrie_polygon=poly,
            bron=feat.get('Bron1'),
            nauwkeurig=feat.get('Nauwkeurig'),
            opmerkingen=feat.get('Opmerkinge'),
            intekening=feat.get('Intekening'),
            datum=feat.get('Datum1')
        )

    def process_row(self, row):

        geom = GEOSGeometry(row['wkt'])

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

    def before(self):
        """
        Cleaning up before reimport
        """
        database.clear_models(models.VerdachtGebied)

    def process_feature(self, feat):
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

        geom = GEOSGeometry(feat.geom.wkt)

        if isinstance(geom, MultiPolygon):
            poly = geom
        elif isinstance(geom, Polygon):
            poly = MultiPolygon(geom)
        else:
            log.error('Geo error')
            raise GEOSGeometry('Unworkable Geos type %s' % geom.geom_type)

        return models.VerdachtGebied(
            kenmerk=feat.get('Kenmerk'),
            type='bommenkaart/verdachtgebied',
            detail_type=feat.get('Hoofdgroep'),
            subtype=feat.get('Subsoort'),

            aantal=feat.get('Aantallen'),
            kaliber=feat.get('Kaliber'),
            verschijning=feat.get('Verschijni'),

            oorlogshandeling=feat.get('Oorlogshan'),
            afbakening=feat.get('Afbakening'),

            horizontaal=feat.get('Horizontal'),
            cartografie=feat.get('Cartografi'),
            opmerkingen=feat.get('Opmerkinge'),
            pdf=self.pdf_link(feat.get('Hyperlink')),

            geometrie_polygon=poly,
        )


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

    def before(self):
        """
        Cleaning up before reimport
        """
        database.clear_models(models.UitgevoerdOnderzoek)

    def process_feature(self, feat):
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

        geom = GEOSGeometry(feat.geom.wkt)

        if isinstance(geom, MultiPolygon):
            poly = geom
        elif isinstance(geom, Polygon):
            poly = MultiPolygon(geom)
        else:
            log.error('Geo error')
            raise GEOSGeometry('Unworkable Geos type %s' % geom.geom_type)

        return models.UitgevoerdOnderzoek(
            kenmerk=feat.get('Kenmerk'),
            type='bommenkaart/uitgevoerdonderzoek',
            detail_type=feat.get('Soort_rapp'),
            onderzoeksgebied=feat.get('Onderzoeks'),
            opdrachtnemer=feat.get('Opdrachtne'),
            opdrachtgever=feat.get('Opdrachtge'),
            verdacht_gebied=feat.get('Verdacht_g'),
            geometrie_polygon=poly,
            datum=feat.get('Datum')
        )

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
        elif isinstance(geom, Polygon):
            poly = MultiPolygon(geom)
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

    path_prefix = 'Bommenkaart'

    def tasks(self):
        return [
            ImportInslagenTask(path=os.path.join(self.path_prefix, INSLAGEN_PATH)),
            ImportVerdachtGebiedTask(path=os.path.join(self.path_prefix, VERDACHTE_GEBIEDEN_PATH)),
            ImportUitgevoerdOnderzoekTask(path=os.path.join(self.path_prefix, UITGEVOERD_ONDERZOEK_PATH)),
            ImportGevrijwaardTask(path=os.path.join(self.path_prefix, GEVRIJWAARD_GEBIED_PATH)),
        ]
