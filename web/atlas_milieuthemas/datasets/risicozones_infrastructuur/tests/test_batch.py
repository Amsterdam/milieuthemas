# Project
from datapunt_generic.batch.test import TaskTestCase
from .. import batch, models


class ImportAardgasbuisleidingTest(TaskTestCase):
    def task(self):
        return batch.ImportAardgasbuisleidingTask()

    def test_import(self):
        self.run_task()

        imported = models.Aardgasbuisleiding.objects.count()
        self.assertEqual(9, imported)

        aard_leiding = models.Aardgasbuisleiding.objects.get(pk=4)
        self.assertNotEqual(aard_leiding.geometrie, None)

class ImportASpoorwegTest(TaskTestCase):
    def task(self):
        return batch.ImportSpoorwegTask()

    def test_import(self):
        self.run_task()

        imported = models.Spoorweg.objects.count()
        self.assertEqual(1, imported)

        spoorweg = models.Spoorweg.objects.get(pk=1)
        self.assertNotEqual(spoorweg.geometrie, None)