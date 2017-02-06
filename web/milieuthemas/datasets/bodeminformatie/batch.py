import logging
import os

from django.contrib.gis.geos import GEOSGeometry

from datapunt_generic.batch import batch
from datapunt_generic.generic import database
from datapunt_generic.generic.csv import process_csv, parse_decimal, \
    parse_datum, parse_nummer
from . import models

log = logging.getLogger(__name__)


class ImportGrondmonster(batch.BasicTask):
    name = "Import dmb_grondmonster"
    model = models.Grondmonster

    def before(self):
        database.clear_models(models.Grondmonster)

    def process(self):
        source = os.path.join(self.path, "dmb_grondmonster.csv")
        monsters = [monster for monster in process_csv(source, self.process_row)
                    if monster]

        models.Grondmonster.objects.bulk_create(monsters,
                                                batch_size=database.BATCH_SIZE)

    def process_row(self, row):
        try:
            rapportdatum = parse_datum(row['rapportdatum'])
        except ValueError as msg:
            log.warning("Grondmonster {} unable to parse date {}; skipping".format(
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


class ImportGrondwatermonster(batch.BasicTask):
    name = "Import dmb_watermonster"
    model = models.Grondwatermonster

    def before(self):
        database.clear_models(models.Grondwatermonster)

    def process(self):
        source = os.path.join(self.path, "dmb_watermonster.csv")
        monsters = [monster for monster in process_csv(source, self.process_row)
                    if monster]

        models.Grondwatermonster.objects.bulk_create(monsters,
                                                     batch_size=database.BATCH_SIZE)

    def process_row(self, row):
        return models.Grondwatermonster(
            geo_id=parse_nummer(row['id']),
            locatie=row['locatienaam'],
            type_onderzoek=row['type_onderzoek'],
            rapportnummer=row['rapportnummer'],
            naam_boring=row['naam_boring'],
            grondwaterstand=parse_nummer(row['grondwaterstand']),
            naam_monster=row['naam_monster'],
            bovenkant=parse_nummer(row['bovenkant']),
            onderkant=parse_nummer(row['onderkant']),
            eindoordeel=row['eindoordeel'],
            dichloorethaan_11=parse_decimal(row['dichloorethaan_11']),
            dichlooretheen_11=parse_nummer(row['dichlooretheen_11']),
            trichloorethaan_111=parse_nummer(row['trichloorethaan_111']),
            trichloorethaan_112=parse_nummer(row['trichloorethaan_112']),
            dichloorethaan_12=parse_nummer(row['dichloorethaan_12']),
            dichlooretheen_12=parse_nummer(row['dichlooretheen_12']),
            dichloorpropaan_12=parse_nummer(row['dichloorpropaan_12']),
            dichloorpropeen_13=parse_nummer(row['dichloorpropeen_13']),
            arseen=parse_nummer(row['arseen']),
            barium=parse_nummer(row['barium']),
            benzeen=parse_nummer(row['benzeen']),
            cadmium=parse_nummer(row['cadmium']),
            chloride=parse_nummer(row['chloride']),
            chloroform=parse_nummer(row['chloroform']),
            cis_dichlooretheen_12=parse_nummer(row['cis_dichlooretheen_12']),
            cobalt=parse_nummer(row['cobalt']),
            dichloorbenzenen=parse_nummer(row['dichloorbenzenen']),
            dichloormethaan=parse_nummer(row['dichloormethaan']),
            ethylbenzeen=parse_nummer(row['ethylbenzeen']),
            koper=parse_nummer(row['koper']),
            kwik=parse_nummer(row['kwik']),
            lood=parse_nummer(row['lood']),
            minerale_olie=parse_nummer(row['minerale_olie']),
            molybdeen=parse_nummer(row['molybdeen']),
            monochloorbenzeen=parse_nummer(row['monochloorbenzeen']),
            naftaleen=parse_nummer(row['naftaleen']),
            nikkel=parse_nummer(row['nikkel']),
            ph=parse_nummer(row['ph']),
            styreen=parse_nummer(row['styreen']),
            tetrachlooretheen=parse_nummer(row['tetrachlooretheen']),
            tetrachloormethaan=parse_nummer(row['tetrachloormethaan']),
            tolueen=parse_nummer(row['tolueen']),
            trans_dichlooretheen_12=parse_nummer(
                row['trans_dichlooretheen_12']),
            tribroommethaan=parse_nummer(row['tribroommethaan']),
            trichlooretheen=parse_nummer(row['trichlooretheen']),
            trichloormethaan=parse_nummer(row['trichloormethaan']),
            vinylchloride=parse_nummer(row['vinylchloride']),
            xylenen=parse_nummer(row['xylenen']),
            zink=parse_nummer(row['zink']),
            xcoordinaat=parse_nummer(row['xcoordinaat']),
            ycoordinaat=parse_nummer(row['ycoordinaat']),
            geometrie=GEOSGeometry(row['geometrie']),
        )


class ImportAsbest(batch.BasicTask):
    name = "Import dmb_asbest"
    model = models.Asbest

    def before(self):
        database.clear_models(models.Asbest)

    def process(self):
        source = os.path.join(self.path, "dmb_asbest.csv")
        asbest = [asbest for asbest in process_csv(source, self.process_row) if
                  asbest]

        models.Asbest.objects.bulk_create(asbest,
                                          batch_size=database.BATCH_SIZE)

    def process_row(self, row):
        return models.Asbest(
            geo_id=parse_nummer(row['id']),
            locatie=row['locatienaam'],
            type_onderzoek=row['type_onderzoek'],
            xcoordinaat=parse_nummer(row['xcoordinaat']),
            ycoordinaat=parse_nummer(row['ycoordinaat']),
            naam_boring=row['naam_boring'],
            naam_monster=row['naam_monster'],
            materiaal=row['materiaal'],
            bovenkant=parse_nummer(row['bovenkant']),
            onderkant=parse_nummer(row['onderkant']),
            monster_mengmonster=row['monster_mengmonster'],
            concentratie=parse_nummer(row['concentratie']),
            stof=row['stof'],
            geometrie=GEOSGeometry(row['geometrie']),
        )


class ImportBodeminformatieJob(object):
    name = "Import bodeminformatie"

    def tasks(self):
        return [
            ImportGrondmonster(),
            ImportGrondwatermonster(),
            ImportAsbest(),
        ]
