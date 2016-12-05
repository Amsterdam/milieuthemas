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
from datapunt_generic.generic.csv import process_csv, parse_nummer

log = logging.getLogger(__name__)


class ImportLPGStationTask(batch.BasicTask):
    name = "Import dmb_lpg_station"
    model = models.LPGStation

    points = dict()

    def before(self):
        source = os.path.join(self.path, "dmb_lpg_station_punten.csv")
        process_csv(source, self.process_point_row)

        database.clear_models(models.LPGStation)

    def process_point_row(self, row):
        self.points[row['stationnummer']] = row['geometrie']

    def after(self):
        self.points.clear()
        super().after()

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
    model = models.LPGVulpunt

    def before(self):
        database.clear_models(models.LPGVulpunt)
        self.stations = frozenset(models.LPGStation.objects.all().values_list('pk', flat=True))

    def after(self):
        self.stations = None
        super().after()

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
    stations = set()
    model = models.LPGAfleverzuil

    def before(self):
        database.clear_models(models.LPGAfleverzuil)
        self.stations = frozenset(models.LPGStation.objects.all().values_list('pk', flat=True))

    def after(self):
        self.stations = None
        super().after()

    def process(self):
        source = os.path.join(self.path, "dmb_lpg_afleverzuil.csv")
        zuilen = [zuil for zuil in process_csv(source, self.process_row) if zuil]

        models.LPGAfleverzuil.objects.bulk_create(zuilen, batch_size=database.BATCH_SIZE)

    def process_row(self, row):
        station_id = int(row['stationnummer'])

        if station_id not in self.stations:
            log.warn("LPGAfleverzuil references an unknown station {}; skipping".format(
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
            log.warn("LPGAfleverzuil {} unable to encapsulate GEOS geometry {}; skipping".format(
                row['id'],
                msg,
            ))
            return

        return models.LPGAfleverzuil(
            station_id=station_id,
            geometrie_point=point,
            geometrie_polygon=poly,
        )


class ImportLPGTankTask(batch.BasicTask):
    name = "Import dmb_lpg_tank"
    stations = set()
    model = models.LPGTank

    def before(self):
        database.clear_models(models.LPGTank)
        self.stations = frozenset(models.LPGStation.objects.all().values_list('pk', flat=True))

    def after(self):
        self.stations = None
        super().after()

    def process(self):
        source = os.path.join(self.path, "dmb_lpg_tank.csv")
        tanks = [tank for tank in process_csv(source, self.process_row) if tank]

        models.LPGTank.objects.bulk_create(tanks, batch_size=database.BATCH_SIZE)

    def process_row(self, row):
        if not row['type_contour']:
            return

        station_id = int(row['stationnummer'])

        if station_id not in self.stations:
            log.warn("LPGTank references an unknown station {}; skipping".format(
                    station_id,
            ))
            return

        geom = GEOSGeometry(row['geometrie'])

        if isinstance(geom, Polygon):
            geom = MultiPolygon(geom)

        return models.LPGTank(
            station_id=station_id,
            kleur=parse_nummer(row['kleur'] or 0),
            type=row['type_contour'],
            voldoet=row['voldoet'],
            afstandseis=row['afstandseis'],
            geometrie=geom,
        )


class ImportBronTask(batch.BasicTask):
    name = "Import dmb_veilig_bronnen"
    model = models.Bron

    def before(self):
        database.clear_models(models.Bron)

    def process(self):
        source = os.path.join(self.path, "dmb_veilig_bronnen.csv")
        bronnen = [bron for bron in process_csv(source, self.process_row) if bron]

        models.Bron.objects.bulk_create(bronnen, batch_size=database.BATCH_SIZE)

    def process_row(self, row):
        # Making bron id a requirement
        if not row['bron_id']:
            log.warn("Bron has an empty bron_id; skipping")
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


class ImportBedrijfTask(batch.BasicTask):
    name = "Import dmb_veilig_bedrijven"
    points = dict()
    model = models.Bedrijf

    def before(self):
        source = os.path.join(self.path, "dmb_veilig_bedr_punten.csv")
        process_csv(source, self.process_point_row)

        database.clear_models(models.Bedrijf)

    def process_point_row(self, row):
        self.points[row['id']] = row['geometrie']

    def after(self):
        self.points.clear()
        super().after()

    def process(self):
        source = os.path.join(self.path, "dmb_veilig_bedrijven.csv")
        bedrijven = [bedrijf for bedrijf in process_csv(source, self.process_row) if bedrijf]

        models.Bedrijf.objects.bulk_create(bedrijven, batch_size=database.BATCH_SIZE)

    def process_row(self, row):
        # Making company name a requirement
        if not row['bedrijfsnaam']:
            log.warn("Bedrijf has an empty bedrijfsnaam; skipping")
            return

        geom = GEOSGeometry(row['geometrie'])

        if isinstance(geom, Polygon):
            geom = MultiPolygon(geom)

        point = None
        try:
            point = GEOSGeometry(self.points[row['id']])
        except (GEOSException, KeyError):
            pass

        return models.Bedrijf(
            bedrijfsnaam=row['bedrijfsnaam'],
            adres=row['adres'],
            stadsdeel=row['stadsdeel'],
            aantal_bronnen=row['aantal_bronnen'],
            bevoegd_gezag=row['bevoegd_gezag'],
            categorie_bevi=row['categorie_bevi'],
            type_bedrijf=row['type_bedrijf'],
            opmerkingen=row['opmerkingen'],
            geometrie_polygon=geom,
            geometrie_point=point,
        )


class ImportContourTask(batch.BasicTask):
    name = "Import dmb_veilig_contouren"
    model = models.Contour

    def before(self):
        database.clear_models(models.Contour)

    def process(self):
        source = os.path.join(self.path, "dmb_veilig_contouren.csv")
        contouren = [contour for contour in process_csv(source, self.process_row) if contour]

        models.Contour.objects.bulk_create(contouren, batch_size=database.BATCH_SIZE)

    def process_row(self, row):
        # Making bron id a requirement
        if not row['bron_id']:
            log.warn("Bron has an empty bron_id; skipping")
            return

        geom = GEOSGeometry(row['geometrie'])

        if isinstance(geom, Polygon):
            geom = MultiPolygon(geom)

        return models.Contour(
            bron_id=row['bron_id'],
            bedrijfsnaam=row['bedrijfsnaam'],
            type_contour=row['type_contour'],
            afstandseis=row['afstandseis'],
            voldoet=row['voldoet'],
            geometrie=geom,
        )


class ImportRisicozonesBedrijvenJob(object):
    name = "Import risicozones bedrijven"

    def tasks(self):
        return [
            ImportLPGStationTask(),
            ImportLPGVulpuntTask(),
            ImportLPGAfleverzuilTask(),
            ImportLPGTankTask(),
            ImportBronTask(),
            ImportBedrijfTask(),
            ImportContourTask(),
        ]
