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