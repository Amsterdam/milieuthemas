# Python
import logging
import os
# Packages
from django.contrib.gis.geos import GEOSGeometry, MultiPolygon, Point, Polygon
from django.contrib.gis.geos.error import GEOSException
# Project
from . import models
from datapunt_generic.batch import batch
from datapunt_generic.generic import database
from datapunt_generic.generic.csv import process_csv

log = logging.getLogger(__name__)


# ID need to be taken from the csv to enable data matching between all the sources
class ImportBrisantbomTask(batch.BasicTask):
    name = "import dmb_brisantbom"

    def before(self):
        """
        Cleaning up before reimport
        """
        database.clear_models(models.Brisantbom)

    def after(self):
        """
        No cleanup werk needed
        """
        pass

    def process(self):
        """
        Processing the CSV
        """
        source = os.path.join(self.path, "dmb_brisantbom.csv")
        brisantbommen = [brisantbom for brisantbom in process_csv(source, self.process_row) if brisantbom]
        models.Brisant.bulk_create(bristabommen, batch_size=database.BATCH_SIZE)

    def process_row(self, row):
        if 'id' not in row or not row['id']:
            print('No id, skipping')
        else:
            print(row['id'])
        return None


class ImportBrisantbomJob(object):
    name = "Import bristabommen informatie"

    def tasks(self):
        return[
            ImportBrisantbomTask(),
        ]
