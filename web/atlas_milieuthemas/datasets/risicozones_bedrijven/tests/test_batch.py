from datapunt_generic.batch.test import TaskTestCase
from .. import batch, models


class ImportLPGVulpuntTest(TaskTestCase):
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
