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


class ImportGeluidzoneTask(batch.BasicTask):
    name = "Import dro_geluid"
    themas = set()
    models = {
        models.Spoorwegen: list(),
        models.Metro: list(),
        models.Industrie: list(),
    }

    def before(self):
        for model in self.models.keys():
            database.clear_models(model)

        self.themas = frozenset(Thema.objects.values_list('id', flat=True))

    def after(self):
        self.themas = None

    def process(self):
        source = os.path.join(self.path, "dro_geluid.csv")
        process_csv(source, self.process_row)

        for model, import_models in self.models.items():
            model.objects.bulk_create(import_models, batch_size=database.BATCH_SIZE)

    def process_row(self, row):
        model, geluid_zone_type = None, row['type'].lower()

        if 'spoorwegen' in geluid_zone_type:
            model = models.Spoorwegen

        if 'metro' in geluid_zone_type:
            model = models.Metro

        if 'industrie' in geluid_zone_type:
            model = models.Industrie

        if not model:
            log.warn("Geluidzone {} unable to determine model for type {}; skipping"
                     .format(row['id'], geluid_zone_type))
            return

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

        result = model(
            geo_id=int(row['id']),
            type=row['type'],
            thema_id=thema_id,
            geometrie=geom,
        )

        if 'industrie' in row['type'].lower():
            result.naam = row['naam_industrieterrein']

        self.models[model].append(result)


class ImportGeluidzoneJob(object):
    name = "Import geluidzone"

    def tasks(self):
        return [
            ImportGeluidzoneTask(),
        ]
