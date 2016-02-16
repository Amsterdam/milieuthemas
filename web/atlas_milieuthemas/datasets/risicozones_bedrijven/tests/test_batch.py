from datapunt_generic.batch.test import TaskTestCase
from .. import batch, models

from . import factories


class ImportLPGStationTest(TaskTestCase):
    def task(self):
        return batch.ImportLPGStationTask()

    def test_import(self):
        self.run_task()

        imported = models.LPGStation.objects.all()
        self.assertEqual(len(imported), 17)

        station = models.LPGStation.objects.get(id=11)
        self.assertEqual(station.bedrijfsnaam, 'BIKHARI RETAIL ENTERPRISE BV')
        self.assertNotEqual(station.geometrie_polygon, None)
        self.assertNotEqual(station.geometrie_point, None)


class ImportLPGVulpuntTest(TaskTestCase):
    def setUp(self):
        factories.LPGStationFactory.create(pk=1)
        factories.LPGStationFactory.create(pk=14)

    def task(self):
        return batch.ImportLPGVulpuntTask()

    def test_import(self):
        self.run_task()

        imported = models.LPGVulpunt.objects.all()
        self.assertEqual(len(imported), 2)

        vulpunt = models.LPGVulpunt.objects.get(geo_id=2)
        self.assertEqual(vulpunt.type, 'Vulpunt')
        self.assertNotEqual(vulpunt.geometrie_point, None)
        self.assertEqual(vulpunt.geometrie_polygon, None)

        vulpunt = models.LPGVulpunt.objects.get(geo_id=69)
        self.assertEqual(vulpunt.type, 'Plaatsgebonden risico 10-5')
        self.assertEqual(vulpunt.geometrie_point, None)
        self.assertNotEqual(vulpunt.geometrie_polygon, None)


class ImportLPGAfleverzuilTest(TaskTestCase):
    def task(self):
        return batch.ImportLPGAfleverzuilTask()

    def test_import(self):
        self.run_task()

        imported = models.LPGAfleverzuil.objects.all()
        self.assertEqual(len(imported), 3)

        zuilen = models.LPGAfleverzuil.objects.filter(stationnummer=27)
        self.assertEqual(len(zuilen), 2)
        self.assertNotEqual(zuilen[0].geometrie_polygon, None)
        self.assertNotEqual(zuilen[1].geometrie_point, None)

        zuil = models.LPGAfleverzuil.objects.get(stationnummer=26)
        self.assertNotEqual(zuil.geometrie_polygon, None)
        self.assertEqual(zuil.geometrie_point, None)


class ImportLPGTankTest(TaskTestCase):
    def task(self):
        return batch.ImportLPGTankTask()

    def test_import(self):
        self.run_task()

        imported = models.LPGTank.objects.all()
        self.assertEqual(len(imported), 2)

        tank = models.LPGTank.objects.get(stationnummer=19)
        self.assertEqual(tank.type, 'Invloedsgebied groepsrisico opslagtank')
        self.assertNotEqual(tank.geometrie, None)


class ImportBronTest(TaskTestCase):
    def task(self):
        return batch.ImportBron()

    def test_import(self):
        self.run_task()

        imported = models.Bron.objects.count()
        self.assertEqual(imported, 13)

        bron = models.Bron.objects.get(bron_id=24)
        self.assertEqual(bron.bedrijfsnaam, 'NUSTAR TERMINAL BV')
        self.assertEqual(bron.hoeveelheid_stof, '615.000 m3')
        self.assertEqual(bron.type_stof, 'BENZINE EN ANDERE AARDOLIEFRACTIES')


class ImportBedrijfTest(TaskTestCase):
    def task(self):
        return batch.ImportBedrijf()

    def test_import(self):
        self.run_task()

        imported = models.Bedrijf.objects.count()
        self.assertEqual(imported, 15)

        bedrijf = models.Bedrijf.objects.filter(bedrijfsnaam='DIERGAARDE CHEMICAL STORAGE').first()
        self.assertEqual(bedrijf.stadsdeel, 'Westpoort')
        self.assertEqual(bedrijf.categorie_bevi, 'EMBALLAGE, art.2.1.f')
        self.assertNotEqual(bedrijf.geometrie_polygon, None)
