import logging
import os

from django.conf import settings

from datapunt_generic.batch import batch
from datapunt_generic.generic import database

from datapunt_generic.generic.csv import process_csv
from . import models

log = logging.getLogger(__name__)


class ImportThemaTask(batch.BasicTask):
    name = "Import dro_thema"

    def before(self):
        database.clear_models(models.Thema)

    def after(self):
        pass

    def process(self):
        source = os.path.join(self.path, "dro_thema.csv")
        themas = process_csv(source, self.process_row)

        models.Thema.objects.bulk_create(themas, batch_size=database.BATCH_SIZE)

    def process_row(self, row):
        return models.Thema(
            id=int(row['thema_id']),
            type=row['type'],
            toelichting=row['toelichting'],
            wet_of_regelgeving=row['wet_of_regelgeving'],
            datum_laatste_wijziging=row['datum_laatste_wijziging'],
            disclaimer=row['disclaimer'],
            informatie=row['informatie'],
        )


class ImportThemasJob(object):
    name = "Import themas"

    def tasks(self):
        return [
            ImportThemaTask(),
        ]
