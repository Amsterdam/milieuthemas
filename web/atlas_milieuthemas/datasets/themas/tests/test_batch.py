from datapunt_generic.batch.test import TaskTestCase
from .. import batch, models

DIRECTORY = 'diva/milieuthemas'


class ImportThemaTest(TaskTestCase):
    def task(self):
        return batch.ImportThemaTask(DIRECTORY)

    def test_import(self):
        self.run_task()

        imported = models.Thema.objects.all()
        self.assertEqual(len(imported), 10)

        vlak = models.Thema.objects.get(pk=7)
        self.assertEqual(vlak.type, 'Vogelvrijwaringsgebied Schiphol')
