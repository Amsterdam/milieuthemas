import logging
import os

from django.contrib.gis.geos import GEOSGeometry, Point, Polygon, MultiPolygon
from django.contrib.gis.geos.error import GEOSException

from datapunt_generic.batch import batch
from datapunt_generic.generic import database

from datapunt_generic.generic.csv import process_csv, parse_nummer
from . import models

log = logging.getLogger(__name__)


class ImportLPGStationTask(batch.BasicTask):
    name = "Import dmb_lpg_station"
    points = dict()

    def before(self):
        source = os.path.join(self.path, "dmb_lpg_station_punten.csv")
        process_csv(source, self.process_point_row)

        database.clear_models(models.LPGStation)

    def process_point_row(self, row):
        self.points[row['stationnummer']] = row['geometrie']

    def after(self):
        self.points.clear()

    def process(self):
        source = os.path.join(self.path, "dmb_lpg_station.csv")
        stations = [station for station in process_csv(source, self.process_row) if station]

        models.LPGStation.objects.bulk_create(stations, batch_size=database.BATCH_SIZE)

    def process_row(self, row):
        if not row['dossiernummer']:
            return

        geom = GEOSGeometry(row['geometrie'])

        if isinstance(geom, Polygon):
            geom = MultiPolygon(geom)

        return models.LPGStation(
            id=int(row['stationnummer']),
            dossiernummer=row['dossiernummer'],
            bedrijfsnaam=row['bedrijfsnaam'],
            adres=row['adres'],
            postcode=row['postcode'],
            plaats=row['plaats'],
            oliemaatschappij=row['oliemaatschappij'],
            omzet=row['omzet'],
            ligging=row['ligging'],
            tank_aanwezig=row['tank_aanwezig'],
            tank_positie=row['tank_positie'],
            tank_inhoud=row['tank_inhoud'],
            vulpunt_aanwezig=row['vulpunt_aanwezig'],
            vulmoment=row['vulmoment'],
            opmerkingen=row['opmerkingen'],
            geometrie_polygon=geom,
            geometrie_point=GEOSGeometry(self.points[row['stationnummer']]),
        )


class ImportLPGVulpuntTask(batch.BasicTask):
    name = "Import dmb_lpg_vulpunt"
    stations = set()

    def before(self):
        database.clear_models(models.LPGVulpunt)
        self.stations = frozenset(models.LPGStation.objects.all().values_list('pk', flat=True))

    def after(self):
        pass

    def process(self):
        source = os.path.join(self.path, "dmb_lpg_vulpunt.csv")
        vulpunten = [vulpunt for vulpunt in process_csv(source, self.process_row) if vulpunt]

        models.LPGVulpunt.objects.bulk_create(vulpunten, batch_size=database.BATCH_SIZE)

    def process_row(self, row):
        if not row['id']:
            return

        station_id = int(row['stationnummer'])

        if station_id not in self.stations:
            log.warn("LPGVulpunt {} references an unknown station {}; skipping".format(
                row['id'],
                station_id,
            ))
            return

        point, poly = None, None

        try:
            geom = GEOSGeometry(row['geometrie'])

            if isinstance(geom, Point):
                point = geom

            if isinstance(geom, Polygon):
                poly = MultiPolygon(geom)

            if isinstance(geom, MultiPolygon):
                poly = geom

        except GEOSException as msg:
            log.warn("LPGVulpunt {} unable to encapsulate GEOS geometry {}; skipping".format(
                row['id'],
                msg,
            ))
            return

        return models.LPGVulpunt(
            geo_id=int(row['id']),
            station_id=station_id,
            type=row['type_contour'],
            afstandseis=row['afstandseis'],
            voldoet=row['voldoet'],
            geometrie_point=point,
            geometrie_polygon=poly,
        )


class ImportLPGAfleverzuilTask(batch.BasicTask):
    name = "Import dmb_lpg_afleverzuil"

    def before(self):
        database.clear_models(models.LPGAfleverzuil)

    def after(self):
        pass

    def process(self):
        source = os.path.join(self.path, "dmb_lpg_afleverzuil.csv")
        zuilen = [zuil for zuil in process_csv(source, self.process_row) if zuil]

        models.LPGAfleverzuil.objects.bulk_create(zuilen, batch_size=database.BATCH_SIZE)

    def process_row(self, row):
        point, poly = None, None

        try:
            geom = GEOSGeometry(row['geometrie'])

            if isinstance(geom, Point):
                point = geom

            if isinstance(geom, Polygon):
                poly = MultiPolygon(geom)

            if isinstance(geom, MultiPolygon):
                poly = geom

        except GEOSException as msg:
            log.warn("LPGAfleverzuil {} unable to encapsulate GEOS geometry {}; skipping".format(
                row['id'],
                msg,
            ))
            return

        return models.LPGAfleverzuil(
            stationnummer=parse_nummer(row['stationnummer']),
            geometrie_point=point,
            geometrie_polygon=poly,
        )


class ImportLPGTankTask(batch.BasicTask):
    name = "Import dmb_lpg_tank"

    def before(self):
        database.clear_models(models.LPGTank)

    def after(self):
        pass

    def process(self):
        source = os.path.join(self.path, "dmb_lpg_tank.csv")
        tanks = [tank for tank in process_csv(source, self.process_row) if tank]

        models.LPGTank.objects.bulk_create(tanks, batch_size=database.BATCH_SIZE)

    def process_row(self, row):
        if not row['type_contour']:
            return

        geom = GEOSGeometry(row['geometrie'])

        if isinstance(geom, Polygon):
            geom = MultiPolygon(geom)

        return models.LPGTank(
            stationnummer=parse_nummer(row['stationnummer']),
            kleur=parse_nummer(row['stationnummer'] or 0),
            type=row['type_contour'],
            voldoet=row['voldoet'],
            afstandseis=row['afstandseis'],
            geometrie=geom,
        )


class ImportBron(batch.BasicTask):
    name = "Import dmb_veilig_bronnen"

    def before(self):
        database.clear_models(models.Bron)

    def after(self):
        pass

    def process(self):
        source = os.path.join(self.path, "dmb_veilig_bronnen.csv")
        bronnen = [bron for bron in process_csv(source, self.process_row) if bron]

        models.Bron.objects.bulk_create(bronnen, batch_size=database.BATCH_SIZE)

    def process_row(self, row):
        # Making bron id a requirement
        if not row['bron_id']:
            return

        geom = GEOSGeometry(row['geometrie'])

        if isinstance(geom, Polygon):
            geom = MultiPolygon(geom)

        return models.Bron(
            bron_id=row['bron_id'],
            bedrijfsnaam=row['bedrijfsnaam'],
            hoeveelheid_stof=row['hoeveelheid_stof'],
            type_stof=row['type_stof'],
            geometrie_polygon=geom,
        )

class ImportBedrijf(batch.BasicTask):
    name = "Import dmb_veilig_bedrijven"

    def before(self):
        database.clear_models(models.Bedrijf)

    def after(self):
        pass

    def process(self):
        source = os.path.join(self.path, "dmb_veilig_bedrijven.csv")
        bedrijven = [bedrijf for bedrijf in process_csv(source, self.process_row) if bedrijf]

        models.Bron.objects.bulk_create(bedrijven, batch_size=database.BATCH_SIZE)

    def process_row(self, row):
        # Making company name a requirement
        if not row['bedrijfsnaam']:
            return

        geom = GEOSGeometry(row['geometrie'])

        if isinstance(geom, Polygon):
            geom = MultiPolygon(geom)

        return models.Bron(
            bedrijfsnaam=row['bedrijfsnaam'],
            adres=row['adres'],
            stadsdeel=row['stadsdeel'],
            aantal_bronnen=row['aantal_bronnen'],
            bevoegd_gezag=row['bevoegd_gezag'],
            categorie_bevi=row['categorie_bevi'],
            type_bedrijf=row['type_bedrijf'],
            opmerkingen=row['opmerkingen'],
            geometrie_polygon=geom,
        )


class ImportRisicozonesBedrijvenJob(object):
    name = "Import risicozones bedrijven"

    def tasks(self):
        return [
            ImportLPGVulpuntTask(),
            ImportLPGAfleverzuilTask(),
            ImportLPGTankTask(),
            ImportBron(),
            ImportBedrijf(),
        ]
