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


class AbstractImportGeluidzoneTask(batch.BasicTask):
    name = "Import dro_geluid"
    themas = set()
    model = None

    class Meta:
        abstract = True

    def before(self):
        if not self.model:
            raise ValueError('model must be defined')

        database.clear_models(self.model)
        self.themas = frozenset(Thema.objects.values_list('id', flat=True))

    def after(self):
        self.themas = None

    def process(self):
        if not self.model:
            raise ValueError('model must be defined')

        source = os.path.join(self.path, "dro_geluid.csv")
        zones = [zone for zone in process_csv(source, self.process_row) if zone]

        self.model.objects.bulk_create(zones, batch_size=database.BATCH_SIZE)

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

        return self.model(
            geo_id=int(row['id']),
            type=row['type'],
            thema_id=thema_id,
            geometrie=geom,
        )


class ImportSpoorwegenTask(AbstractImportGeluidzoneTask):
    model = models.Spoorwegen

    def process_row(self, row):
        if 'spoorwegen' in row['type'].lower():
            return super(ImportSpoorwegenTask, self).process_row(row)


class ImportMetroTask(AbstractImportGeluidzoneTask):
    model = models.Metro

    def process_row(self, row):
        if 'metro' in row['type'].lower():
            return super(ImportMetroTask, self).process_row(row)


class ImportIndustrieTask(AbstractImportGeluidzoneTask):
    model = models.Industrie

    def process_row(self, row):
        if 'industrie' in row['type'].lower():
            model = super(ImportIndustrieTask, self).process_row(row)
            model.naam = row['naam_industrieterrein']

            return model


class ImportGeluidzoneJob(object):
    name = "Import geluidzone"

    def tasks(self):
        return [
            ImportSpoorwegenTask(),
            ImportMetroTask(),
            ImportIndustrieTask(),
        ]
