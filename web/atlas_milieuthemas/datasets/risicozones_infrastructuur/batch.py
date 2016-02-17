"""
Batch importing task for the Risicozones infrastructuur
"""

# Python
import logging
import os
# Packages
from django.contrib.gis.geos import GeometryCollection, GEOSGeometry, LineString, MultiLineString, MultiPolygon, Polygon
from django.contrib.gis.geos.error import GEOSException
# Project
from . import models
from datapunt_generic.batch import batch
from datapunt_generic.generic import database
from datapunt_generic.generic.csv import process_csv


log = logging.getLogger(__name__)  # pylint: disable=C0103

class ImportAardgasbuisleidingTask(batch.BasicTask):
    """
    Aardgas buis leiding import task
    """
    name = 'Import dmb_aardgas_leiding'

    def before(self):
        database.clear_models(models.Aardgasbuisleiding)

    def after(self):
        pass

    def process(self):
        source = os.path.join(self.path, 'dmb_aardgas_leiding.csv')
        # Processing csv
        aard_leidingen = [aard_leiding for aard_leiding in process_csv(source, self.process_row) if aard_leiding]
        # Bulk creating valid entries
        models.Aardgasbuisleiding.objects.bulk_create(aard_leidingen, batch_size=database.BATCH_SIZE)

    def process_row(self, row):
        """
        Handle CSV row
        """
        # geometrie is the only actual data. If not present there is no point
        # in importing
        if not row['geometrie']:
            return None
        try:
            geom = GEOSGeometry(row['geometrie'])
            # Converting to a MultiLineString
            if isinstance(geom, LineString):
                geom = MultiLineString([geom])
            elif not isinstance(geom, MultiLineString) and isinstance(geom, GeometryCollection):
                # Converting to MultiLineString
                lines = []
                for item in geom:
                    if isinstance(item, LineString):
                        lines.append(item)
                    elif isinstance(item, Polygon):
                        for poly_item in item:
                            # Line ring are managable
                            if poly_item.geom_type == 'LinearRing':
                                lines.append(LineString(poly_item.coords))
                            else:
                                raise GEOSException('Polygon in GeometryCollection with unmanagable components')
                    else:
                        raise GEOSException('GeometryCollection with unmanagable components')
                geom = MultiLineString(lines)
        except GEOSException as msg:
            log.warn('Aardgasbuisleiding %d unable to encapsulate GEOS geometry %s; skipping', row['id'], msg)
            return None
        return models.Aardgasbuisleiding(geometrie=geom)


class ImportSpoorwegTask(batch.BasicTask):
    """
    Spoorweg import task
    """
    name = 'Import dro_risico_spoorweg'

    def before(self):
        database.clear_models(models.Spoorweg)

    def after(self):
        pass

    def process(self):
        source = os.path.join(self.path, 'dro_risico_spoorweg.csv')
        # Processing csv
        spoorwegen = [spoorweg for spoorweg in process_csv(source, self.process_row) if spoorweg]
        # Bulk creating valid entries
        models.Spoorweg.objects.bulk_create(spoorwegen, batch_size=database.BATCH_SIZE)

    def process_row(self, row):
        """
        Handle CSV row
        """
        # geometrie is the only actual data. If not present there is no point
        # in importing
        if not row['geometrie']:
            return None
        try:
            geom = GEOSGeometry(row['geometrie'])
            # Converting single poly to multi
            if isinstance(geom, Polygon):
                geom = MultiPolygon(geom)
            elif not isinstance(geom, MultiPolygon):
                raise GEOSGeometry('Unworkable Geos type %s' % geom.geom_type)
        except GEOSException as msg:
            log.warn('Aardgasbuisleiding %d unable to encapsulate GEOS geometry %s; skipping', row['id'], msg)
            return None
        return models.Spoorweg(geometrie=geom)


class ImportRisicozonesInfrastructuurJob(object):
    """
    Import tasks listing for the risicozones infrasctuctuur dataset
    """
    name = 'Import risicozones infrastructuur'

    def tasks(self):
        """
        Return the list of tasks to run
        """
        return [
            ImportAardgasbuisleidingTask(),
            ImportSpoorwegTask(),
        ]
