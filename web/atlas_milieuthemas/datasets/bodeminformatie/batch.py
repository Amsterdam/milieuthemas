import logging
import os

from django.contrib.gis.geos import GEOSGeometry
from django.contrib.gis.geos.error import GEOSException

from datapunt_generic.batch import batch
from datapunt_generic.generic import database

from datapunt_generic.generic.csv import process_csv, parse_decimal, parse_datum, parse_nummer
from . import models

log = logging.getLogger(__name__)


class ImportGrondmonster(batch.BasicTask):
    name = "Import dmb_grondmonster"

    def before(self):
        database.clear_models(models.Grondmonster)

    def process(self):
        source = os.path.join(self.path, "dmb_grondmonster.csv")
        monsters = [monster for monster in process_csv(source, self.process_row) if monster]

        models.Grondmonster.objects.bulk_create(monsters, batch_size=database.BATCH_SIZE)

    def process_row(self, row):
        try:
            rapportdatum = parse_datum(row['rapportdatum'])
        except ValueError as msg:
            log.warn("Grondmonster {} unable to parse date {}; skipping".format(
                    row['id'],
                    row['rapportdatum'],
            ))
            return

        return models.Grondmonster(
            geo_id=parse_nummer(row['id']),
            locatie=row['locatienaam'],
            am_nummer=row['am_nummer'],
            type_onderzoek=row['type_onderzoek'],
            rapportnummer=row['rapportnummer'],
            bureau=row['bureau'],
            rapportdatum=rapportdatum,
            naam_boring=row['naam_boring'],
            xcoordinaat=parse_nummer(row['xcoordinaat']),
            ycoordinaat=parse_nummer(row['ycoordinaat']),
            grondwaterstand=parse_nummer(row['grondwaterstand']),
            naam_monster=row['naam_monster'],
            materiaal=row['materiaal'],
            bovenkant=parse_decimal(row['bovenkant']),
            onderkant=parse_nummer(row['onderkant']),
            eindoordeel=row['eindoordeel'],
            monster_mengmonster=row['monster_mengmonster'],
            lutum=parse_decimal(row['lutum']),
            organische_stof=parse_nummer(row['organische_stof']),
            cadmium=parse_nummer(row['cadmium']),
            kwik=parse_nummer(row['kwik']),
            koper=parse_nummer(row['koper']),
            nikkel=parse_nummer(row['nikkel']),
            lood=parse_nummer(row['lood']),
            zink=parse_nummer(row['zink']),
            chroom=parse_nummer(row['chroom']),
            arseen=parse_nummer(row['arseen']),
            pak=parse_nummer(row['pak']),
            eox=parse_nummer(row['eox']),
            pcb=parse_nummer(row['pcb']),
            minerale_olie=parse_nummer(row['minerale_olie']),
            geometrie=GEOSGeometry(row['geometrie']),
        )


class ImportBodeminformatieJob(object):
    name = "Import bodeminformatie"

    def tasks(self):
        return [
            ImportGrondmonster(),
        ]
