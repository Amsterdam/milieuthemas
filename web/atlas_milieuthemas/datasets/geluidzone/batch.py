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
    models = dict()

    def before(self):
        self.models = {
            'spoorwegen': {
                'model': models.Spoorwegen,
                'models': list(),
            },
            'metro': {
                'model': models.Metro,
                'models': list(),
            },
            'industrie': {
                'model': models.Industrie,
                'models': list(),
            }
        }

        [database.clear_models(self.models[key]['model']) for key in self.models.keys()]

        self.themas = frozenset(Thema.objects.values_list('id', flat=True))

    def after(self):
        self.themas = None

    def process(self):
        source = os.path.join(self.path, "dro_geluid.csv")
        process_csv(source, self.process_row)

        # noinspection PyUnresolvedReferences
        [
            self.models[key]['model'].objects.bulk_create(self.models[key]['models'], batch_size=database.BATCH_SIZE)
            for key in self.models.keys()
        ]

    def process_row(self, row):
        model = None
        geluid_zone_type = row['type'].lower()

        try:
            model_key = [k for k in self.models.keys() if k in geluid_zone_type][0]
        except IndexError:
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

        # noinspection PyCallingNonCallable
        row_model = self.models[model_key]['model'](
                geo_id=int(row['id']),
                type=row['type'],
                thema_id=thema_id,
                geometrie=geom,
        )

        if model_key == 'industrie':
            row_model.naam = row['naam_industrieterrein']

        # noinspection PyUnresolvedReferences
        self.models[model_key]['models'].append(row_model)


class ImportGeluidzoneJob(object):
    name = "Import geluidzone"

    def tasks(self):
        return [
            ImportGeluidzoneTask(),
        ]
