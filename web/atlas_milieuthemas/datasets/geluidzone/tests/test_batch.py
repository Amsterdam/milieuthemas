from datapunt_generic.batch.test import TaskTestCase
from .. import batch, models

from datasets.themas.tests.factories import ThemaFactory


class ImportSpoorwegenTest(TaskTestCase):
    def setUp(self):
        ThemaFactory.create(pk=1)

    def task(self):
        return batch.ImportSpoorwegenTask()

    def test_import(self):
        self.run_task()

        imported = models.Spoorwegen.objects.all()
        self.assertEqual(len(imported), 1)

        zone = models.Spoorwegen.objects.get(geo_id=12)
        self.assertEqual(zone.type, 'Geluidszone spoorwegen')
        self.assertNotEqual(zone.geometrie, None)


class ImportMetroTest(TaskTestCase):
    def setUp(self):
        ThemaFactory.create(pk=1)

    def task(self):
        return batch.ImportMetroTask()

    def test_import(self):
        self.run_task()

        imported = models.Metro.objects.all()
        self.assertEqual(len(imported), 1)

        zone = models.Metro.objects.get(geo_id=11)
        self.assertEqual(zone.type, 'Geluidszone metro')
        self.assertNotEqual(zone.geometrie, None)


class ImportIndustrieTest(TaskTestCase):
    def setUp(self):
        ThemaFactory.create(pk=10)

    def task(self):
        return batch.ImportIndustrieTask()

    def test_import(self):
        self.run_task()

        imported = models.Industrie.objects.all()
        self.assertEqual(len(imported), 1)

        zone = models.Industrie.objects.get(geo_id=25)
        self.assertEqual(zone.naam, 'AMC Zuidoost')
        self.assertNotEqual(zone.geometrie, None)
